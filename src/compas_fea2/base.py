from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib
import uuid
from abc import abstractmethod
from typing import Iterable
from copy import deepcopy
import numpy as np
import h5py

from compas.data import Data

import compas_fea2

from .utilities._utils import to_dimensionless
import json


class DimensionlessMeta(type):
    """Metaclass for converting pint Quantity objects to dimensionless."""

    def __new__(meta, name, bases, class_dict):
        # Decorate each method
        for attributeName, attribute in class_dict.items():
            if callable(attribute) or isinstance(attribute, (classmethod, staticmethod)):
                # Unwrap classmethod/staticmethod to decorate the underlying function
                if isinstance(attribute, (classmethod, staticmethod)):
                    original_func = attribute.__func__
                    decorated_func = to_dimensionless(original_func)
                    # Re-wrap classmethod/staticmethod
                    attribute = type(attribute)(decorated_func)
                else:
                    attribute = to_dimensionless(attribute)
                class_dict[attributeName] = attribute
        return type.__new__(meta, name, bases, class_dict)


class FEAData(Data, metaclass=DimensionlessMeta):
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
        """Try to get the backend plug-in implementation, otherwise use the base
        one.
        """
        imp = compas_fea2._get_backend_implementation(cls)
        if not imp:
            return super(FEAData, cls).__new__(cls)
        return super(FEAData, imp).__new__(imp)

    def __init__(self, name=None, **kwargs):
        self.uid = uuid.uuid4()
        super().__init__()
        self._name = name or "".join([c for c in type(self).__name__ if c.isupper()]) + "_" + str(id(self))
        self._registration = None
        self._key = None

    @property
    def key(self):
        return self._key

    @property
    def input_key(self):
        if self._key is None:
            raise AttributeError(f"{self!r} does not have a key.")
        if self._registration is None:
            raise AttributeError(f"{self!r} is not registered to any part.")
        # if self._registration._key is None:
        #     raise AttributeError(f"{self._registration!r} is not registered to a model.")
        return self._key  # + self._registration._key + self.model._starting_key

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, id(self))

    def __str__(self):
        title = "compas_fea2 {0} object".format(self.__class__.__name__)
        separator = "-" * (len(title))
        data_extended = []
        for a in list(filter(lambda a: not a.startswith("__") and not a.startswith("_") and a != "jsondefinitions", dir(self))):
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

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)

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

    # ==========================================================================
    # Copy and Serialization
    # ==========================================================================
    def copy(self, cls=None, copy_guid=False, copy_name=False):
        """Make an independent copy of the data object.

        Parameters
        ----------
        cls : Type[:class:`compas.data.Data`], optional
            The type of data object to return.
            Defaults to the type of the current data object.
        copy_guid : bool, optional
            If True, the copy will have the same guid as the original.

        Returns
        -------
        :class:`compas.data.Data`
            An independent copy of this object.

        """
        if not cls:
            cls = type(self)
        obj = cls.__from_data__(deepcopy(self.__data__))
        if copy_name and self._name is not None:
            obj._name = self.name
        if copy_guid:
            obj._guid = self.guid
        return obj  # type: ignore

    def to_hdf5(self, hdf5_path, group_name, mode="w"):
        """
        Save the object to an HDF5 file using the __data__ property.
        """
        with h5py.File(hdf5_path, mode) as hdf5_file:  # "a" mode to append data
            group = hdf5_file.require_group(f"{group_name}/{self.uid}")  # Create a group for this object

            for key, value in self.to_hdf5_data().items():
                if isinstance(value, (list, np.ndarray)):
                    group.create_dataset(key, data=value)
                else:
                    group.attrs[key] = json.dumps(value)
                

    @classmethod
    def from_hdf5(
        cls,
        hdf5_path,
        group_name,
        uid,
    ):
        """
        Load an object from an HDF5 file using the __data__ property.
        """
        with h5py.File(hdf5_path, "r") as hdf5_file:
            group = hdf5_file[f"{group_name}/{uid}"]
            data = {}

            # Load datasets (numerical values)
            for key in group.keys():
                dataset = group[key][:]
                data[key] = dataset.tolist() if dataset.shape != () else dataset.item()

            # Load attributes (strings, dictionaries, JSON lists)
            for key, value in group.attrs.items():
                if isinstance(value, str):
                    # Convert "None" back to NoneType
                    if value == "None":
                        data[key] = None
                    # Convert JSON back to Python objects
                    elif value.startswith("[") or value.startswith("{"):
                        try:
                            data[key] = json.loads(value)
                        except json.JSONDecodeError:
                            data[key] = value  # Keep it as a string if JSON parsing fails
                    else:
                        data[key] = value
                else:
                    data[key] = value

        if not hasattr(cls, "__from_data__"):
            raise NotImplementedError(f"{cls.__name__} does not implement the '__from_data__' method.")
        return cls.__from_data__(data)

    def to_json(self, filepath, pretty=False, compact=False, minimal=False):
        """Convert an object to its native data representation and save it to a JSON file.

        Parameters
        ----------
        filepath : str
            The path to the JSON file.
        pretty : bool, optional
            If True, format the output with newlines and indentation.
        compact : bool, optional
            If True, format the output without any whitespace.
        minimal : bool, optional
            If True, exclude the GUID from the JSON output.

        """
        json.dump(self.__data__, open(filepath, "w"), indent=4)
