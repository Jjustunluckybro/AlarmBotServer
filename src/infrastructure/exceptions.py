class InfrastructureException(Exception):
    ...


class AlarmNotRepeatable(InfrastructureException):
    ...


class UnexpectedInfrastructureException(InfrastructureException):
    ...
