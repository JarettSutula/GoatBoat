#!/usr/bin/env python3

"""
.. include:: ../README.md
.. include:: ../AUTHORS.md
.. include:: ../CHANGELOG.md
"""
from os import path
from . import __version__ as version_info

import logging
import logging.config


"""
Warning:
The fileConfig() function takes a default parameter, disable_existing_loggers, 
which defaults to True for reasons of backward compatibility. 

This may or may not be what you want, since it will cause any non-root loggers
existing before the fileConfig() call to be disabled unless 
they (or an ancestor) are explicitly named in the configuration. 

Please refer to the reference documentation for more information, 
and specify False for this parameter if you wish.

So, bring in the config before the creating an instance of the logger
"""

# Goes before getting the logger
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)

# Goes after loading the config
_logger = logging.getLogger(__name__)

__version__ = version_info.__version__
__author__ = version_info.__author__
__author_email__ = version_info.__author_email__
__title__ = version_info.__title__
__description__ = version_info.__description__
__url__ = version_info.__url__
__build__ = version_info.__build__
__license__ = version_info.__license__
__copyright__ = version_info.__copyright__
__keywords__ = version_info.__keywords__
__project_urls__ = version_info.__project_urls__


__all__ = ["examples"]