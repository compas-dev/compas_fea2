from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.base import Base


class FEABase(Base):
    """Base class for all FEA model objects.

    This base class inherits the serialisation infrastructure
    from the base class for core COMPAS objects: :class:`compas.base.Base`.

    It adds the abstract functionality for the representation of FEA objects
    in a model and/or problem summary,
    and for their representation in software-specific calculation files.

    Examples
    --------
    >>>

    """

    def __str__(self):
        """String representation of the object.

        This method is used to explicitly convert the object to a string, with :func:``str``,
        or implicitly, using the print function.

        Returns
        -------
        str

        Examples
        --------
        Convert the object to a string.
        This returns a value.

        >>> s = str(obj)
        >>> s
        '...'

        Print the object.
        This does not return a value.

        >>> p = print(obj)
        '...'
        >>> p
        None
        """
        title = 'compas_fea2 {0} object'.format(self.__name__)
        separator = '-' * (len(title))
        data_extended = []
        for a in list(filter(lambda a: not a.startswith('__') and not a.startswith('_') and a != 'jsondefinitions', dir(self))):
            try:
                if not callable(getattr(self, a)):
                    data_extended.append('{0:<15} : {1}'.format(a, getattr(self, a)))
            except:
                pass
        return """\n{}\n{}\n{}\n""".format(title, separator, '\n'.join(data_extended))

    def __repr__(self):
        """Code representation of object.

        This method is used to convert the object to a code representation that can be evaluated by :func:`eval`
        to recreate the object.

        Returns
        -------
        str

        Examples
        --------
        >>> str(obj) == str(eval(repr(obj)))
        True
        """
        raise NotImplementedError

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file.

        Returns
        -------
        str

        Examples
        --------
        >>>
        """
        raise NotImplementedError
