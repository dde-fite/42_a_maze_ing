# NAME

MiniLibX - Managing windows

# SYNOPSYS

    void *

**mlx_new_window** ( *void \*mlx_ptr, unsigned int width, unsigned int
height, const char \*title* );

    int

**mlx_clear_window** ( *void \*mlx_ptr, void \*win_ptr* );

    int

**mlx_destroy_window** ( *void \*mlx_ptr, void \*win_ptr* );

# DESCRIPTION

The **mlx_new_window** () function creates a new window on the screen,
using the *width* and *height* parameters to determine its size, and
*title* as the text that should be displayed in the window\'s title bar.
The *mlx_ptr* parameter is the connection identifier returned by
**mlx_init** () (see the **mlx** man page). **mlx_new_window** ()
returns a *void \** window identifier that can be used by other MiniLibX
calls. Note that the MiniLibX can handle an arbitrary number of separate
windows.

**mlx_clear_window** () and **mlx_destroy_window** () respectively clear
(in black) and destroy the given window. They both have the same
parameters: *mlx_ptr* is the screen connection identifier, and *win_ptr*
is a window identifier.

# RETURN VALUES

If **mlx_new_window()** fails to create a new window (whatever the
reason), it will return NULL, otherwise a non-null pointer is returned
as a window identifier. **mlx_clear_window** and **mlx_destroy_window**
return nothing.

# SEE ALSO

mlx(3), mlx_pixel_put(3), mlx_new_image(3), mlx_loop(3), mlx_extra(3)

# AUTHOR

Copyright ol@ - 2002-2025 - Olivier Crouzet
