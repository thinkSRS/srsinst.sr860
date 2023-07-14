##! 
##! Copyright(c) 2023 Stanford Research Systems, All rights reserved
##! Subject to the MIT License
##! 

import logging
from srsgui import Task
from .sr860 import SR860

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
