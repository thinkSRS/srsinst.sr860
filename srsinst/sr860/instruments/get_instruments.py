import logging
from srsgui import Task
from .sr860 import SR860
from .sr865 import SR865
from .sr865a import SR865A

logger = logging.getLogger(__name__)


def get_sr860(task: Task, name=None) -> SR860:
    """
    Instead of using task.get_instrument() directly in a Task subclass,
    Defining a wrapper function with a instrument return type will help
    a context-sensitive editors display  attributes available
    for the instrument class.
    """
    if name is None:
        inst = list(task.inst_dict.values())[0]
    else:
        inst = task.get_instrument(name)

    if issubclass(type(inst), SR860):
        return inst
    else:
        logger.error('{} is not {}'.format(type(inst), SR860))
        return None


def get_sr865(task: Task, name=None) -> SR865:
    if name is None:
        inst = list(task.inst_dict.values())[0]
    else:
        inst = task.get_instrument(name)

    if issubclass(type(inst), SR865):
        return inst
    else:
        logger.error('{} is not {}'.format(type(inst), SR865))
        return None


def get_sr865a(task: Task, name=None) -> SR865A:
    if name is None:
        inst = list(task.inst_dict.values())[0]
    else:
        inst = task.get_instrument(name)

    if issubclass(type(inst), SR865A):
        return inst
    else:
        logger.error('{} is not {}'.format(type(inst), SR865A))
        return None
