class DBException(Exception):
    ...


class DBNotFound(DBException):
    ...


class DuplicateKey(DBException):
    ...
