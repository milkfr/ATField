from app import celery
from app.models.tasks import Task
import json


@celery.task(bind=True)
def do_async_scan(self, func_type, time_type, command, targets, description):
    # 新增任务
    task = Task.insert_task_and_return(func_type=func_type, time_type=time_type, command=command,
                                       targets=targets, description=description, celery_id=self.request.id)
    task.update_process("running")
    result = None
    # 执行任务
    if func_type == Task.FUNC_TYPES[0]:
        from . import domain_resolution
        result = domain_resolution.do_scan(targets=targets)
    elif func_type == Task.FUNC_TYPES[1]:
        pass
    # 更新结果
    task.update_result(result=json.dumps(result["result"]), start_time=result["start_time"], end_time=result["end_time"])
    # send_email
