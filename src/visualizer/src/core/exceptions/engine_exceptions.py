class EngineException(Exception):
    pass


class EngineNotStarted(EngineException):
    pass


class EngineElementNotFound(EngineException):
    pass


class EngineElementConflict(EngineException):
    pass
