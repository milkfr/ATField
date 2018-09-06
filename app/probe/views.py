from . import probe


@probe.route("/host/list")
def host_list():
    #
    pass


@probe.route("/host/update")
def host_update():
    pass


@probe.route("/net/list")
def service_list():
    pass


@probe.route("/net/update")
def service_update():
    pass


@probe.route("/app/list")
def app_list():
    pass


@probe.route("/app/update")
def app_update():
    pass
