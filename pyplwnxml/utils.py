import re

from aenum import Enum


def regex_escaped_joined_enum_values(enum: Enum) -> str:
    return "|".join([re.escape(q.value) for q in enum])
def list_intersection(lst1, lst2):
    return list(filter(lambda item: item in lst2, lst1))