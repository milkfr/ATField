import uuid
from .. import db


class Host(db.Model):
    __tablename__ = "hosts"
    id = db.Column(db.String(32), primary_key=True)
    ip = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    status = db.Column(db.String(10))
    services = db.relationship("Service", backref="host")
    host_domain = db.relationship("HostDomain", backref="host")

    def __repr__(self):
        return "<Host {} {}>".format(self.ip, self.name)

    def __init__(self, **kwargs):
        super(Host, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    @staticmethod
    def insert_items(host_info_list):
        # host_info_list = [{"ip": None, "name": None, "description": None}, {...}]
        for host_info in host_info_list:
            host = Host(ip=host_info["ip"], name=host_info["name"], description=host_info["description"])
            db.session.add(host)
        db.session.commit()

    def update_probe_info(self, status):
        self.status = status
        db.session.add(self)
        db.session.commit()

    def update_info(self, name, description):
        self.name = name
        self.description = description
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        for service in self.services:
            db.session.delete(service)
        for hd in HostDomain.query.filter(HostDomain.host == self).all():
            db.session.delete(hd)
        db.session.delete(self)
        db.session.commit()


class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.String(32), primary_key=True)
    port = db.Column(db.Integer, unique=True)
    tunnel = db.Column(db.String(32))
    protocol = db.Column(db.String(32))
    state = db.Column(db.String(10))
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    host_id = db.Column(db.String(32), db.ForeignKey("hosts.id"))

    def __repr__(self):
        return "<Service {} {} {} {}>".format(self.port, self.tunnel, self.protocol, self.name)

    def __init__(self, **kwargs):
        super(Service, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    @staticmethod
    def insert_items(service_info_list):
        # service_info_list = [{"ip": None, "port": None, "tunnel": None, "protocol": None,
        # "state": None, "name": None, "description": None}, {...}]
        for service_info in service_info_list:
            host = Host.query.filter(Host.ip == service_info["ip"]).first()
            service = Service(host=host, port=service_info["port"], tunnel=service_info["tunnel"],
                              protocol=service_info["protocol"], state=service_info["state"],
                              name=service_info["name"], description=service_info["description"])
            db.session.add(service)
        db.session.commit()

    def update_info(self, name, description):
        self.name = name
        self.description = description
        db.session.add(self)
        db.session.commit()

    def update_probe_info(self, tunnel, protocol, state):
        self.tunnel = tunnel
        self.tunnel = protocol
        self.state = state
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()


class Domain(db.Model):
    __tablename__ = "domains"
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    host_domain = db.relationship("HostDomain", backref="domain")

    def __repr__(self):
        return "<Domain {}>".format(self.name)

    def __init__(self, **kwargs):
        super(Domain, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    @staticmethod
    def insert_items(domain_info_list):
        # domain_info_list = [{"name": None, "description", None}, {...}]
        for domain_info in domain_info_list:
            domain = Domain(name=domain_info["name"], description=domain_info["description"])
            db.session.add(domain)
            db.session.commit()

    def update_probe_info(self, ips):
        # ips = ["0.0.0.1", "1.1.1.1"]
        for hd in HostDomain.query.filter(HostDomain.doamin == self).all():
            db.session.delete(hd)
        for ip in ips:
            host = Host.query.filter(Host.ip == ip).first()
            hd = HostDomain(host=host, domain=self)
            db.session.add(hd)
        db.session.commit()

    def update_info(self, name, description):
        self.name = name
        self.description = description
        db.session.add()
        db.session.commit()

    def delete_item(self):
        HostDomain.delete_relationship_by_domain(self)
        db.session.delete(self)
        db.session.commit()


class HostDomain(db.Model):
    __tablename__ = "host_domain"
    id = db.Column(db.String(32), primary_key=True)
    host_id = db.Column(db.String(32), db.ForeignKey("hosts.id"))
    domain_id = db.Column(db.String(32), db.ForeignKey("domains.id"))

    def __repr__(self):
        return "<HostDomain {}<->{}>".format(self.host, self.domain)

    def __init__(self, **kwargs):
        super(HostDomain, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())
