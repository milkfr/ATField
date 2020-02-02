### 环境搭建
#### 机器
VMware安装Linux Ubuntu 18.04虚拟机

先安装vamware-tools，点击vmware的安装vmware-tools，执行里面的`vmware-install.pl`文件，然后重启

安装其他软件

```
$ sudo passwd  # 修改密码
$ sudo apt-get update  # 更新源
$ sudo apt-get upgrade
$ sudo apt-get install fcitx-googlepinyin  # 添加中文输入法，之后在System Settings里配置一下fcitx，重启系统，再在右上角键盘图标里的Configure选项里添加google-pinyin选项，修改快捷切换的方式，就可以使用了
$ sudo apt-get install vim  # 安装vim
$ sudo apt-get install git  # 安装git
$ git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"  # 添加神奇的git log别名
```

#### IDE
JetBrains官网下载Toolbox，安装PyCharm、WebStorm

#### frontend
```
$ wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash  # 搭建nvm环境
$ nvm install 10.15.3  # 下载最新稳定版node
$ npm config set registry https://registry.npm.taobao.org  # npm改淘宝镜像
$ npm install -g vue-cli  # 安全vue-cli
$ vue init webpack frontend  # 初始化vue前端项目,安装了vue，vue-router等依赖
$ npm i element-ui -S  # 安装element-ui
$ npm install axios  # 安装axios
$ npm install axios-mock-adapter mockjs --save-dev  # 安装dev模式下的mock
```

#### backend
```
$ sudo apt-get install python3-pip
$ pip3 install --user pipenv
$ mkdir backend
$ pipenv --python 3
$ export FLASK_APP=manager.py
$ export FLASK_ENV=development
$ export flask run
```
