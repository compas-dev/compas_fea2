from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from typing import Iterable
from compas.data import Data
import compas_fea2
import importlib

from abc import abstractmethod


class FEAData(Data):
    """Base class for all FEA model objects.

    This base class inherits the serialisation infrastructure
    from the base class for core COMPAS objects: :class:`compas.base.`.

    It adds the abstract functionality for the representation of FEA objects
    in a model and/or problem summary,
    and for their representation in software-specific calculation files.

    Parameters
    ----------
    name : str, optional
        The name of the object, by default None. If not provided, one is automatically
        generated.

    Attributes
    ----------
    name : str
        The name of the object.
    registration : compas_fea2 object
        The mother object where this object is registered to.

    """

    def __new__(cls, *args, **kwargs):
        imp = compas_fea2._get_backend_implementation(cls)
        if not imp:
            return super(FEAData, cls).__new__(cls)
        return super(FEAData, imp).__new__(imp)

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self._name = name or "".join([c for c in type(self).__name__ if c.isupper()]) + "_" + str(id(self))
        self._registration = None

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, id(self))

    def __str__(self):
        title = "compas_fea2 {0} object".format(self.__class__.__name__)
        separator = "-" * (len(title))
        data_extended = []
        for a in list(
            filter(lambda a: not a.startswith("__") and not a.startswith("_") and a != "jsondefinitions", dir(self))
        ):
            try:
                attr = getattr(self, a)
                if not callable(attr):
                    if not isinstance(attr, Iterable):
                        data_extended.append("{0:<15} : {1}".format(a, attr.__repr__()))
                    else:
                        data_extended.append("{0:<15} : {1}".format(a, len(attr)))
            except Exception:
                pass
        return """\n{}\n{}\n{}\n""".format(title, separator, "\n".join(data_extended))

    @abstractmethod
    def jobdata(self, *args, **kwargs):
        """Generate the job data for the backend-specific input file."""
        raise NotImplementedError("This function is not available in the selected plugin.")

    @classmethod
    def from_name(cls, name, **kwargs):
        """Create an instance of a class of the registered plugin from its name.

        Parameters
        ----------
        name : str
            The name of the class (without the `_` prefix)

        Returns
        -------
        obj
            The wanted object

        Notes
        -----
        By convention, only hidden class can be called by this method.

        """
        obj = cls(**kwargs)
        module_info = obj.__module__.split(".")
        obj = getattr(importlib.import_module(".".join([*module_info[:-1]])), "_" + name)
        return obj(**kwargs)
