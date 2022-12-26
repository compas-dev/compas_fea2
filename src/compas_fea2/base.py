from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data import Data
import compas_fea2
import importlib


class FEAData(Data):
    """Base class for all FEA model objects.

    This base class inherits the serialisation infrastructure
    from the base class for core COMPAS objects: :class:`compas.base.`.

    It adds the abstract functionality for the representation of FEA objects
    in a model and/or problem summary,
    and for their representation in software-specific calculation files.

    Examples
    --------
    >>>

    """

    def __init__(self, name=None):
        """Base class for all FEA2 objects.

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
        super().__init__()
        # NOTE the names length in abaqus is limited to 80 characters
        self._name = name or ''.join([c for c in type(self).__name__ if c.isupper()])+"_"+str(id(self))
        self._registration = None

    def __new__(cls, *args, **kwargs):
        """Try to get the backend plug-in implementation, otherwise use the base
        one.
        """
        imp = compas_fea2._get_backend_implementation(cls)
        if not imp:
            return super(FEAData, cls).__new__(cls)
        return super(FEAData, imp).__new__(imp)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, id(self))

    def jobdata(self):
        raise NotImplementedError('This function is not available in the selected plugin.')

    # TODO maybe not useful anymore..? change 'element'
    @classmethod
    def from_name(cls, name, **kwargs):
        """Create an instance of a class of the registered plugin from its name.

        Note
        ----
        By convention, only hidden class can be called by this method.

        Parameters
        ----------
        name : str
            The name of the class (without the `_` prefix)

        Returns
        -------
        cls
            The wanted class
        """
        element = cls(**kwargs)
        module_info = element.__module__.split('.')
        element = getattr(importlib.import_module('.'.join([*module_info[:-1]])), '_'+name)
        return element(**kwargs)

    def data(self):
        pass

    # def __str__(self):
    #     """String representation of the object.

    #     This method is used to explicitly convert the object to a string, with :func:``str``,
    #     or implicitly, using the print function.

    #     Returns
    #     -------
    #     str

    #     Examples
    #     --------
    #     Convert the object to a string.
    #     This returns a value.

    #     >>> s = str(obj)
    #     >>> s
    #     '...'

    #     Print the object.
    #     This does not return a value.

    #     >>> p = print(obj)
    #     '...'
    #     >>> p
    #     None
    #     """
    #     title = 'compas_fea2 {0} object'.format(self.__class__.__name__)
    #     separator = '-' * (len(title))
    #     data_extended = []
    #     for a in list(filter(lambda a: not a.startswith('__') and not a.startswith('_') and a != 'jsondefinitions', dir(self))):
    #         try:
    #             attr = getattr(self, a)
    #             if not callable(attr):
    #                 if not isinstance(attr, (list, dict, tuple)):
    #                     data_extended.append('{0:<15} : {1}'.format(a, attr.__repr__()))
    #                 else:
    #                     data_extended.append('{0:<15} : {1}'.format(a, attr))
    #         except Exception:
    #             pass
    #     return """\n{}\n{}\n{}\n""".format(title, separator, '\n'.join(data_extended))
