"""Custom exceptions."""


class QtNodesError(Exception):
    """Base custom exception."""


class UnregisteredNodeClassError(QtNodesError):
    """The Node class is not registered."""


class UnknownFlowError(QtNodesError):
    """The flow style can not be recognized."""


class KnobConnectionError(QtNodesError):
    """Something went wrong while trying to connect two Knobs."""
