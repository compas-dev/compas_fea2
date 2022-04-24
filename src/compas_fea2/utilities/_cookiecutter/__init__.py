import os
from .scanner import scan_package
from .scanner import mirror_package


COOKIECUTTER_TEMPLATES = os.path.join(os.path.dirname(__file__), '_templates')
