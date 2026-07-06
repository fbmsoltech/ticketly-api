class ApplicationError(Exception):
    """Base class for application service errors."""


class ResourceNotFoundError(ApplicationError):
    """Raised when a requested resource does not exist."""


class ResourceAlreadyExistsError(ApplicationError):
    """Raised when a resource conflicts with an existing one."""


class AuthenticationError(ApplicationError):
    """Raised when authentication fails."""


class AuthorizationError(ApplicationError):
    """Raised when authorization fails."""
