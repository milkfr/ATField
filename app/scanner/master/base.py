from celery import chord
from celery_worker import celery
import abc
from scanner.node.node import handle


class BaseHandleTask(celery.Task, metaclass=abc.ABCMeta):

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
                tasks.append(handle.s(target, plugin))
        chord(tasks)(self.get_success_callback().s().on_error(self.get_error_callback().s()))

    @abc.abstractmethod
    def get_success_callback(self):
        pass

    @abc.abstractmethod
    def get_error_callback(self):
        pass
