from mlx import Mlx
from ctypes import c_void_p, c_uint, c_char_p, byref
from ..exceptions import MlxException, MlxNotFound


class MlxContext:
    """Bridge between the graphics engine and the Mlx library.

    Stores the instance of the mlx Python wrapper class and the pointer to it \
        at the class level.

    Each time any information related to the library is accessed, the \
        connection is validated to prevent unsuccessful accesses.

    It also contains some new deprecated MLX functions.

    Raises:
        MlxException: In case of an error by MiniLibX itself.
        MlxNotFound: For using a function without having initialized the \
            connection.
    """
    __mlx: Mlx | None = None
    __mlx_ptr: c_void_p | None = None

    @classmethod
    def init(cls) -> None:
        """Instanciates the wrapper and opens the connection with the MLX"""
        cls.__mlx = Mlx()
        if not cls.__mlx:
            raise MlxException("Error opening 'libmlx.so'")
        cls.__mlx_ptr = cls.__mlx.mlx_init()
        if not cls.__mlx_ptr:
            raise MlxException("Error initiating Mlx")

    @classmethod
    def close(cls) -> None:
        """Closes the conection with the MLX"""
        if not cls.__mlx or not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        cls.__mlx.mlx_release(cls.__mlx_ptr)
        del cls.__mlx_ptr
        del cls.__mlx

    @classmethod
    def get_mlx(cls) -> Mlx:
        """Exposes the MLX instance"""
        if not cls.__mlx:
            raise MlxNotFound("Mlx is not initiated")
        return cls.__mlx

    @classmethod
    def get_mlx_ptr(cls) -> c_void_p:
        """Returns the pointer to Mlx"""
        if not cls.__mlx or not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        return cls.__mlx_ptr
