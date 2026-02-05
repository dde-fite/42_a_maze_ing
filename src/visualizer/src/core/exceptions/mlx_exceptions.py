class MlxException(Exception):
    """Error from Mlx"""
    pass


class MlxNotFound(MlxException):
    """Access to an Mlx resource without a connection"""
    pass
