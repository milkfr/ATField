### 0x00 引子
扫描器怎么样用的爽，用甲方我的经验来说

* 资产结构完成，不用更改资产的属性字段变化
* 应急新增了一个PoC，插件写好传上去就可以，运行结果和效果都直接访问Web可以看到，写PoC不需要考虑关心输入输出，可以解耦
* 有漏报误报了可以马上到ES查看所有记录，分析起来方便
* 运营需要添加新的通知，改改`prehandle`和`callback`不需要考虑其他，这里解耦
* 网络编程改写方便，PoC进程、线程、协程变化不需要重新适配、重新部署
* PoC写完容易让人看懂，方便迁移或者改写到别人自己喜欢到框架里

我写的扫描器不一样有多好，比起别的有多少特色，但是也是我经验的结晶，我用的还算爽

可以看我写的两篇经验之谈

[黑盒扫描器自研之路（一）——侃侃构架](https://milkfr.github.io/%E5%AE%89%E5%85%A8%E5%BC%80%E5%8F%91/2018/11/10/dev-black-box-scanner-1/)

[黑盒扫描器自研之路（二）——侃侃功能](https://milkfr.github.io/%E5%AE%89%E5%85%A8%E5%BC%80%E5%8F%91/2018/11/11/dev-black-box-scanner-2/)

我的扫描器不能短平快，也没有把PoC开源，不能开箱即用，需要明白结构和代码，但是理解了，我觉得做甲方自研用起来应该还可以

### 0x01 构架
![构架图](https://github.com/milkfr/ATField/blob/master/structure.png)

```
.
├── app  # API后台和扫描器
│   ├── app  # flask web api
│   ├── celery_worker.py  # celery启动文件
│   ├── config.py  # 配置文件
│   ├── gunicorn.py  # gunicorn文件
│   ├── logs  # 日志文件
│   ├── manager.py  # app启动文件
│   ├── requirements.txt  # Python依赖版本
│   └── scanner  # 扫描器
│       ├── __init__.py  # 注册celery任务的位置
│       ├── master  # celery_master节点的任务
│       ├── node  # celery_node节点的任务
│       └── plugin # 编写PoC的位置
│           └── __init__.py  # 注册PoC的位置
├── conf
│   ├── docker
│   ├── nginx
│   └── supervisor
└── web  # 前端
```

### 0x02 如何写PoC
PoC和Celery结合，分成`prehandle`、`callback`和`PoC`三部分

`prehandle`用来预处理资产和PoC插件，比如分网络做处理等

`PoC`就是扫描任务

`callback`用来处理扫描结果，比如更新资产，提交SIEM等

#### 和Celery结合的部分
```
class BaseHandleTask(celery.Task, metaclass=abc.ABCMeta):

    name = 'master_base'

    @abc.abstractmethod
    def get_target_list(self, target_option):
        pass

    @abc.abstractmethod
    def get_plugin_list(self, plugin_option):
        pass

    def run(self, target_option, plugin_option):
        target_list = self.get_target_list(target_option)
        plugin_list = self.get_plugin_list(plugin_option)
        tasks = []
        for plugin in plugin_list:
            for target in target_list:
                tasks.append(handle.s(target, plugin, self.name))
        chord(tasks)(self.get_success_callback().s().on_error(self.get_error_callback().s()))

    @abc.abstractmethod
    def get_success_callback(self):
        pass

    @abc.abstractmethod
    def get_error_callback(self):
        pass
```

`prehandle`和`callback`的处理通过继承上面这个类`scanner/master/base.py`

我们写一个nmap扫描的功能试试

我们在`scanner/master`目录下写个新文件`special_nmap.py`

```
from scanner.master.base import BaseHandleTask
from app.models.asset import Host
from celery_worker import celery
from app.models import db
from libnmap.parser import NmapParser


class SpecialNmapHandleTask(BaseHandleTask):

    name = 'master_special_nmap_handle'

    def get_target_list(self, target_option):
        db.session.close()
        target_list = [{
            'uid': None,
            'target': ' '.join([host.ip
                                for host in Host.list_items_paginate_by_search(**target_option).items])
        }]
        return target_list

    def get_plugin_list(self, plugin_option):
        plugin_list = [{'name': 'special_nmap', 'option': plugin_option.get('special_nmap')}]
        return plugin_list

    def get_success_callback(self):
        return callback_success

    def get_error_callback(self):
        return callback_error


@celery.task
def callback_success(results):
    parser_result = NmapParser.parse_fromstring(results[0].get('result'))
    for host in parser_result.hosts:
        services = []
        for service in host.services:
            if service.state == 'open':
                services.append({
                    'host_ip': host.address,
                    'port': service.port,
                    'protocol': service.protocol,
                    'tunnel': service.tunnel,
                    'name': service.service_dict.get('name'),
                    'cpe': ' '.join(service.service_dict.get('cpelist', [])),
                    'info': {
                        'status': service.state,
                        'banner': service.banner,
                        'fingerprint': service.servicefp[:500],
                        'product': service.service_dict.get('product'),
                        'version': service.service_dict.get('version'),
                        'extra': service.service_dict.get('extrainfo'),
                    }
                })
        try:
            os_match = host.os_match_probabilities()[0]
        except Exception as e:
            os_match = None
        with db.auto_commit():
            item = Host.get_item_by_ip(host.address)
            if item:
                item.update(
                    service_count=len(services),
                    cpe=' '.join(os_match.get_cpe()) if os_match else '',
                    info={
                        'status': host.status,
                        'hostname': ' '.join(host.hostnames),
                        'system': os_match.name if os_match else '',
                        'mac': host.mac,
                        'accuracy': os_match.accuracy if os_match else 0,
                        'fingerprint': host.os_fingerprint[:500]
                    },
                    services=services
                )


@celery.task
def callback_error(request, exc, traceback):
    print(request, exc, traceback)
```

这个`prehandle`和`callback`都是更新nmap识别前后的资产

可以看到`callback`里还用到了`libnmap`，这里没有做解耦，是因为nmap的扫描结果就是任务结果，`callback`解析结果并转换资产的表，这样解析可以更灵活

然后在`scanner/__init__.py`注册任务

```
from scanner.master.special_nmap import SpecialNmapHandleTask

master_special_nmap_handle = celery.tasks.register(SpecialNmapHandleTask())
```

#### PoC编写
比如redis未授权PoC

在`scanner/plugin/service/redis_unauth.py`中写

```
import socket


def handle(target, option):
    host = target.get('ip')
    port = int(target.get('port'))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(3)
        s.connect((host, port))
        s.send(b'INFO\r\n')
        if b'redis_version' in s.recv(1024):
            return True
    except Exception as e:
        return str(e)
    finally:
        s.close()
```

PoC写的简单点，不依赖任何框架写到类，只用target和option两个参数，方便别人看懂，或者把PoC迁移或者改写到他自己喜欢的框架中

然后在`scanner/plugin/__init__.py`中注册PoC

```
from .service.redis_unauth import handle as service_redis_unauth
```

### 0x03 环境搭建
这里使用阿里云的Ubuntu 18.04为例

#### 获取项目
```
$ git clone https://github.com/milkfr/ATField.git
```

#### 依赖应用环境
按照开发环境的版本，依赖

```
mysql:8.0.19
rabbitmq:3.8.2
redis:5.0.7
elasticsearch:6.8.6
kibana:6.8.6
```

可以用docker安装依赖，根据`conf/docker`文件下的配置，按照自身情况进行修改，比如原本有，就不用了

根据[docker官方文档](https://docs.docker.com/)或者[DaoCloud 软件中心](https://download.daocloud.io/)安装`docker`和`docker-compose`，如果获取镜像速度慢需要修改镜像地址

运行`docker-compose up`即可完成以上5个依赖

mysql需要提前建立数据库

elasticsearch启动可能内存不足，修改`/etc/sysctl.conf`，添加`vm.max_map_count=262144`，运行`sysctl -p`生效

其他一般开箱即用

#### web环境
根据[nvm](https://github.com/nvm-sh/nvm)GitHub地址的指示安装nvm环境，并配置环境变量

```
$ nvm install 10.15.3  # 安装node
$ npm config set registry https://registry.npm.taobao.org  # 改淘宝镜像
$ cd ATField/web  # 切换到web环境
$ vim .env  # 添加env环境变量如下

NODE_ENV=production
VUE_APP_PREVIEW=false
VUE_APP_API_BASE_URL=/api

$ npm install  # 安装依赖
$ npm run build  # 编译前端，完成后dist文件夹内容为我们所需
```

#### app环境
根据[pyenv](https://github.com/pyenv/pyenv)GitHub地址的指示安装pyenv环境，并配置环境变量

根据[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)GitHub地址的指示安装pyenv环境，并配置环境变量

```
# pyenv install的速度很慢，可以新建文件夹~/.pyenv/cache，从Python官网下载好对应版本的tar.xz文件，放在这个目录中，就不用下载可以直接安装
$ sudo apt-get install gcc build-essential zlib1g-dev libbz2-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev  # python安装容易缺少依赖
$ pyenv install 3.8.0  # 确定python版本
$ pyenv virtualenv 3.8.0 atfield-venv  # 创建虚拟环境
$ cd ATField/app  # 切换到app环境
$ pyenv activate atfield-venv  # 启动虚拟环境
$ pip install -r requirements.txt  # 下载python依赖
$ vim .env  # 添加env环境变量如下

FLASK_SECRET_KEY=123456
FLASK_SQLALCHEMY_DATABASE_URI=mysql+cymysql://mysql:mysql@127.0.0.1:3306/atfield
FLASK_CELERY_BROKER_URL=amqp://guest:guest@127.0.0.1:5672/atfield
FLASK_CELERY_BROKER_URL=redis://:redis@127.0.0.1:6379/0
FLASK_ES_HOST=127.0.0.1
FLASK_ES_PORT=9500
FLASK_ES_USERNAME=username
FLASK_ES_PASSWORD=password

$ export FLASK_APP=manager.py  # 设置flask应用
$ flask deploy  # 创建数据库表等操作
```

#### supervisor
假设nginx稳定，依赖应用的稳定性有docker负责，supervisor负责我们自己编写的代码的稳定

```
$ sudo apt-get install supervisor  # 安装superivisor
$ cd ATField/conf/supervisor  # 切换到supervisor配置文件
$ cp ./* /etc/supervisor/conf.d  # 将配置拷贝到supervisor的默认配置位置
# 之后修改配置中路径、用户名等参数
$ supervisorctl
supervisor> start atfiled_app
supervisor> start celery_master
supervisor> start celery_node
supervisor> start celery_flower
supervisor> exit
```

#### nginx
根据[nginx官网](http://nginx.org/)提供的方式安装nginx

```
$ cd ATField/conf/nginx # 切换到supervisor配置文件
$ printf "your_username:$(openssl passwd -crypt your_password)\n" > auth  # 生成HTTP Basic Auth的用户名密码配置文件
$ cp ./* /etc/nginx/conf.d  # 将配置拷贝到nginx的默认配置位置
# 之后修改配置中路径、用户名等参数，注意nginx用户不能访问以下目录
$ nginx -t  # 检查配置
$ nginx -s reload  # 启动
```
