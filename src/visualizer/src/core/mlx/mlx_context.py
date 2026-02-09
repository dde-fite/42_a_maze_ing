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
    def get_mlx_ptr(cls) -> c_void_p | None:
        """Returns the pointer to Mlx"""
        if not cls.__mlx or not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        return cls.__mlx_ptr

    @classmethod
    def xpm_to_image(cls, xpm_data: str) -> tuple[c_void_p, int, int]:
        """Recovers the deleted mlx_xpm_to_image function from the wrapper.

        UNSTABLE

        Args:
            mlx_ptr (c_void_p): Pointer to Mlx
            xpm_data (str): XMP data to load

        Returns:
            tuple[c_void_p, int, int]: Tuple of the img point, width and height
        """
        if not cls.__mlx or not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        width = c_uint()
        height = c_uint()
        cls.__mlx.mlx_func.mlx_xpm_file_to_image.argtypes = [
            c_void_p, c_char_p, c_void_p, c_void_p]
        cls.__mlx.mlx_func.mlx_xpm_file_to_image.restype = c_void_p
        img = cls.__mlx.mlx_func.mlx_xpm_file_to_image(
            cls.__mlx_ptr, xpm_data.encode('utf8'),
            byref(width), byref(height))
        if img is not None:
            cls.__mlx._img_height[str(img)] = height.value
        return img
