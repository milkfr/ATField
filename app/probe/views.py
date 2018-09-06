from . import asset



# 资产类型
# IP内外映射
# 域名列表
# 主机列表
# 应用列表


@asset.route("/host/list")
def host_list():
    #
    pass


@asset.route("/host/update")
def host_update():
    pass


@asset.route("/net/list")
def service_list():
    pass


@asset.route("/net/update")
def service_update():
    pass


@asset.route("/app/list")
def app_list():
    pass


@asset.route("/app/update")
def app_update():
    pass
