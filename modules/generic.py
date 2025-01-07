import enum


class BaseEnum(enum.IntEnum):
    """An `Enum` capable of having its members have docstrings.

    Based on https://stackoverflow.com/questions/19330460/how-do-i-put-docstrings-on-enums
    """

    def __new__(cls, *args):
        """Assign values on creation."""
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __eq__(self, obj):
        """Override equality operator to allow comparison with int."""
        if type(self) == type(obj):
            return super().__eq__(obj)
        return self.value == obj

    def __ne__(self, obj):
        """Override inequality operator to allow comparison with int."""
        if type(self) == type(obj):
            return super().__ne__(obj)
        return self.value != obj


class BaseLabelEnum(BaseEnum):
    """ An `Enum` with a label attribute """
    def __new__(cls, *args):
        """Define object out of args."""
        obj = int.__new__(cls)
        obj._value_ = args[0]
        obj._label = ""
        
        if len(args) > 1:
            obj._label = args[1] 

        return obj

    @property
    def label(self) -> str:
        """ Returns the given label for this Enum"""
        return self._label
        
        
