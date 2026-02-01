from mlx import Mlx
from ctypes import c_void_p
from ..exceptions import MlxException, MlxNotFound


class MlxContext:
    __mlx: Mlx | None = None
    __mlx_ptr: c_void_p | None = None

    @classmethod
    def init(cls) -> None:
        cls.__mlx = Mlx()
        cls.__mlx_ptr = cls.__mlx.mlx_init()
        if not cls.__mlx_ptr:
            raise MlxException("Error initiating Mlx")

    @classmethod
    def close(cls) -> None:
        if not cls.__mlx or not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        cls.__mlx.mlx_release(cls.__mlx_ptr)
        del cls.__mlx_ptr
        del cls.__mlx

    @classmethod
    def get_mlx(cls) -> Mlx:
        if not cls.__mlx:
            raise MlxNotFound("Mlx is not initiated")
        return cls.__mlx

    @classmethod
    def get_mlx_ptr(cls) -> c_void_p | None:
        if not cls.__mlx or not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        return cls.__mlx_ptr

    @classmethod
    def close_mlx(cls) -> None:
        if not cls.__mlx or not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        cls.__mlx.mlx_release(cls.__mlx_ptr)
