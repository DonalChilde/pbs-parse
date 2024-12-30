"""FILE: exceptions.py."""


class StoreManagerException(Exception):
    """Exceptions related to using the store."""


class NotInManifestError(StoreManagerException):
    """The requested resource is not listed in the manifest."""


class UnableToLoadError(StoreManagerException):
    """Unable to load resource."""


class StoreOperationError(StoreManagerException):
    """An incorrect store request."""
