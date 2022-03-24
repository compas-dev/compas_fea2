from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data import Data
import compas_fea2


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

    def __new__(cls, *args, **kwargs):
        imp = compas_fea2.get_backend_implementation(cls)
        if not imp:
            return super(FEAData, cls).__new__(cls)
        return super(FEAData, imp).__new__(imp)

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
