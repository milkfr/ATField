import uuid
from datetime import datetime
from .. import db


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.String(36), primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    func_type = db.Column(db.String(50))
    time_type = db.Column(db.String(50))
    description = db.Column(db.String(500))
    targets = db.Column(db.Text)
    result = db.Column(db.Text)

    def __repr__(self):
        return "<Task {} {}>".format(self.func_type, self.time_type)

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    FUNC_TYPE_DOMAIN_RESOLUTION = "domain resolution"
    FUNC_TYPE_SERVICE_PROBE_BY_NMAP = "service probe by nmap"
    FUNC_TYPE_SERVICE_PROBE_BY_MASSCAN = "service probe by masscan"
    FUNC_TYPES = [FUNC_TYPE_DOMAIN_RESOLUTION,
                  FUNC_TYPE_SERVICE_PROBE_BY_MASSCAN,
                  FUNC_TYPE_SERVICE_PROBE_BY_NMAP]

    STATUS_PENDING = "PENDING"
    STATUS_RUNNING = "RUNNING"
    STATUS_END = "END"

    @staticmethod
    def insert_tasks(task_info_list):
        # task_info_list = [{"func_type": None, "time_type": None,
        # "description": None, "targets": list},...]
        for task_info in task_info_list:
            task = Task(tyep=task_info["func_type"], time_type=task_info["time_type"],
                        description=task_info["description"], targets=task_info["targets"])
            task.status = Task.STATUS_PENDING
            task.start_time = datetime.utcnow()
            db.session.add(task)
        db.session.commit()

    @staticmethod
    def insert_task_and_return(func_type, time_type, description, targets):
        task = Task(func_type=func_type, time_type=time_type,
                    targets=targets, description=description)
        task.status = Task.STATUS_PENDING
        task.start_time = datetime.utcnow()
        db.session.add(task)
        db.session.commit()
        return task

    def update_process(self, status):
        self.status = status
        db.session.add(self)
        db.session.commit()

    def update_result(self, result, start_time, end_time):
        self.status = Task.STATUS_END
        self.result = result
        self.start_time = start_time
        self.end_time = end_time
        db.session.add(self)
        db.session.commit()
