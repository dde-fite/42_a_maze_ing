class EngineException(Exception):
    pass


class EngineNotStarted(EngineException):
    """Access to an engine resource without initializing the engine first"""
    pass


class EngineElementNotFound(EngineException):
    """Access to a resourced that does not exist"""
    pass


class EngineElementConflict(EngineException):
    """Conflict when there is a resource allocated with the same name or\
        parameters"""
    pass


class EngineNoReference(EngineException):
    """No owner to allocate a resource"""
    pass
