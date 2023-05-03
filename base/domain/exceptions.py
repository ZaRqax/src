class BusinessLogicException(Exception):
    message: str = 'Business logic error'

    def __init__(self, message: str | None = None):
        if not message:
            message = self.message

        super().__init__(message)


class BusinessRuleTypeException(BusinessLogicException):
    ...


class DomainRuleException(BusinessLogicException):
    ...


class DomainPermissionException(BusinessLogicException):
    ...
