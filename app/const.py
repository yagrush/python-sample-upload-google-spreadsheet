"""
Constant types in Python.
"""

import sys
import errors


class _const:

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise errors.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


sys.modules[__name__] = _const()
