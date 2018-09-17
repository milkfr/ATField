import uuid
from .. import db


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.String(36), primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    elasped = db.Column(db.Float)
    node = db.Column(db.String)
    status = db.Column(db.String(50))
    type = db.Column(db.String(50))
    time_type = db.Column(db.String(50))
    command = db.Column(db.String(500))
    description = db.Column(db.String(500))
    target = db.Column(db.Text)

    def __repr__(self):
        return "<Task {} {}>".format(self.type, self.time_type)

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())
