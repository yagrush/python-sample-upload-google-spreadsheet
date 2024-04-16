"""
Constant types in Python.
"""

import sys
from app.errors import ConstError


class _const:

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


sys.modules[__name__] = _const()
