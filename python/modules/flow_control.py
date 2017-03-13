#! /usr/bin/python

import os, logging

logger = logging.getLogger("flow control")
logger.info("Executing flow_control module.")


def compare_args(arg1, arg2, comparison):
    if comparison == "equal" or comparison == "==":
        if arg1 == arg2:
            return True
    elif comparison == "different" or comparison == "!=":
        if arg1 != arg2:
            return True
    elif (comparison == "greater" or comparison == ">" or 
            comparison == "less" or comparison == "<"):
        if _greater_or_less(arg1, arg2, comparison):
            return True
    else:
        logger.error("Unknown for TASK_IF comparison type: %s", comparison)
    return False

def _greater_or_less(arg1, arg2, comparison):
    try:
        arg1 = int(arg1)
        arg2 = int(arg2)
    except:
        logger.error("Cannot compare if given parameter is greater/less than "
        "another when given arguments are not integers: %s, %s", arg1, arg2)
        return False
    if comparison == "greater" or comparison == ">":
        if arg1 > arg2:
            return True
    else:
        if arg1 < arg2:
            return True
    return False
