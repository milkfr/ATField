import uuid
from .. import db
from datetime import datetime


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    packages = db.relationship("Package", backref="application")
    application_plugin = db.relationship("ApplicationPlugin", backref="application")

    def __repr__(self):
        return "<Application {} {}>".format(self.name, self.description)

    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    def update_plugin_by_id(self, delete_plugin_list, add_plugin_list):
        for plugin_id in delete_plugin_list:
            ap = ApplicationPlugin.query.filter(ApplicationPlugin.application == self,
                                                ApplicationPlugin.plugin_id == plugin_id).first()
            db.session.delete(ap)
        for plugin_id in add_plugin_list:
            ap = ApplicationPlugin(application=self, plugin_id=plugin_id)
            db.session.add(ap)
        db.session.commit()

    @property
    def plugin_list(self):
        return [application_plugin.plugin for application_plugin in self.application_plugin]

    @staticmethod
    def insert_items(application_info_list):
        # application_info_list = [{"name": None, "description": None}, {...}]
        for application_info in application_info_list:
            application = Application(name=application_info["name"], description=application_info["description"])
            db.session.add(application)
        db.session.commit()

    @staticmethod
    def insert_item(name, description, plugin_list):
        application = Application(name=name, description=description)
        db.session.add(application)
        db.session.commit()
        application.update_plugin_by_id(delete_plugin_list=[], add_plugin_list=plugin_list)
        return application

    def update_info(self, name, description, delete_plugin_list, add_plugin_list):
        self.update_plugin_by_id(delete_plugin_list=delete_plugin_list, add_plugin_list=add_plugin_list)
        self.name = name
        self.description = description
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        for package in self.packages:
            db.session.delete(package)
        for ap in ApplicationPlugin.query.filter(ApplicationPlugin.application == self).all():
            db.session.delete(ap)
        db.session.delete(self)
        db.session.commit()


class Package(db.Model):
    __tablename__ = "packages"
    id = db.Column(db.String(36), primary_key=True)
    entrance = db.Column(db.String(50))  # protocol+domain(or host+port)
    path = db.Column(db.UnicodeText)
    method = db.Column(db.String(10))
    status = db.Column(db.Integer)
    request = db.Column(db.UnicodeText)
    response = db.Column(db.UnicodeText)
    remarks = db.Column(db.UnicodeText)
    update_time = db.Column(db.DateTime)
    application_id = db.Column(db.String(36), db.ForeignKey("applications.id"))

    def __repr__(self):
        return "<Package {} {}>".format(self.entrance, self.application)

    def __init__(self, **kwargs):
        super(Package, self).__init__(**kwargs)
        self.update_time = datetime.utcnow()
        self.id = str(uuid.uuid1())

    def update_info(self, status, request, response, remarks):
        self.status = status
        self.request = request
        self.response = response
        self.remarks = remarks
        self.update_time = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def insert_items(package_info_list):
        # service_info_list = [{"application_id": application_id, "entrance": None, "path": None, "method": None,
        # "status": None, "request": None, "response": None, "remarks": None}, {...}]
        for package_info in package_info_list:
            application = Application.query.filter(Application.id == package_info["application_id"]).first()
            package = Package(application=application, entrance=package_info["entrance"], path=package_info["path"],
                              method=package_info["method"], status=package_info["status"],
                              request=package_info["request"], response=package_info["response"],
                              remarks=package_info["remarks"])
            package.update_time = datetime.utcnow()
            db.session.add(package)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()


class Plugin(db.Model):
    __tablename__ = "plugins"
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    content = db.Column(db.UnicodeText)
    application_plugin = db.relationship("ApplicationPlugin", backref="plugin")

    def __repr__(self):
        return "Plugin {} {}".format(self.name, self.description)

    def __init__(self, **kwargs):
        super(Plugin, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    @property
    def application_list(self):
        return [application_plugin.application for application_plugin in self.application_plugin]

    @staticmethod
    def insert_items(plugin_info_list):
        # plugin_info_list = [{"name": None, "description": None, "content": None}, {...}]
        for plugin_info in plugin_info_list:
            plugin = Plugin(name=plugin_info["name"], description=plugin_info["description"],
                            content=plugin_info["content"])
            plugin.update_time = datetime.utcnow()
            db.session.add(plugin)
        db.session.commit()

    @staticmethod
    def insert_item(name, description, content, application_list):
        plugin = Plugin(name=name, description=description, content=content)
        db.session.add(plugin)
        db.session.commit()
        plugin.update_application_by_id(delete_application_list=[], add_application_list=application_list)

    def update_application_by_id(self, delete_application_list, add_application_list):
        for application_id in delete_application_list:
            ap = ApplicationPlugin.query.filter(ApplicationPlugin.plugin == self,
                                                ApplicationPlugin.application_id == application_id).first()
            db.session.delete(ap)
        for application_id in add_application_list:
            ap = ApplicationPlugin(application_id=application_id, plugin=self)
            db.session.add(ap)
        db.session.commit()

    def update_info(self, name, description, content, delete_application_list, add_application_list):
        self.update_application_by_id(delete_application_list=delete_application_list,
                                      add_application_list=add_application_list)
        self.name = name
        self.description = description
        self.content = content
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        for ap in ApplicationPlugin.query.filter(ApplicationPlugin.plugin == self).all():
            db.session.delete(ap)
        db.session.delete(self)
        db.session.commit()


class ApplicationPlugin(db.Model):
    __tablename__ = "application_plugin"
    id = db.Column(db.String(36), primary_key=True)
    application_id = db.Column(db.String(36), db.ForeignKey("applications.id"))
    plugin_id = db.Column(db.String(36), db.ForeignKey("plugins.id"))

    def __repr__(self):
        return "<ApplicationPlugin {}<->{}".format(self.application, self.plugin)

    def __init__(self, **kwargs):
        super(ApplicationPlugin, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())
