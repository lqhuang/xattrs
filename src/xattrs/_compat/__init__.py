# SPDX-License-Identifier: MIT

from sys import version_info

if version_info >= (3, 11):
    from builtins import ExceptionGroup
else:
    from exceptiongroup import ExceptionGroup
