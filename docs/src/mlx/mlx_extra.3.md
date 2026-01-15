# NAME

MiniLibX - Extra functions

# SYNOPSYS

    int

**mlx_mouse_hide** ( *void \*mlx_ptr* );

    int

**mlx_mouse_show** ( *void \*mlx_ptr* );

    int

**mlx_mouse_move** ( *void \*mlx_ptr, int x, int y* );

    int

**mlx_mouse_get_pos** ( *void \*win_ptr, int \*x, int \*y* );

    int

**mlx_do_key_autorepeatoff** ( *void \*mlx_ptr* );

    int

**mlx_do_key_autorepeaton** ( *void \*mlx_ptr* );

    int

**mlx_get_screen_size** ( *void \*mlx_ptr, unsigned int \*width,
unsigned int \*height* );

    int

**mlx_do_sync** ( *void \*mlx_ptr* );

    int

**mlx_sync** ( *void \*mlx_ptr, int cmd, void \*param* );

# MOUSE EXTRA FUNCTIONS

It is possible to show / hide the mouse, and get its current position
without user click or force its position inside a window.

# KEYBOARD EXTRA FUNCTIONS

The auto-repeat mode of the keyboard can be controlled. By default,
auto-repeat is on: multiple \"key pressed\" events are generated every
second until the key is released.

# SCREEN EXTRA FUNCTION

It is possible to retrieve the size of the current screen, even before
the first window is created.

# FLUSH AND SYNC FUNCTIONS

The **mlx_do_sync** function will flush the pending commands to the
graphic subsystems, ensuring nothing is cached on your software\'s side.
On return, there is no guarantee that your commands have been
processed.\
With **mlx_sync** you have more detailed control over the
synchronisation mechanisms. Three different commands are available:\
#define MLX_SYNC_IMAGE_WRITABLE 1\
#define MLX_SYNC_WIN_FLUSH 2\
#define MLX_SYNC_WIN_COMPLETED 3\
The third parameter *param* can be either the image identifier (command
#1) or the window identifier (commands #2 and #3).

# SEE ALSO

mlx(3), mlx_new_window(3), mlx_pixel_put(3), mlx_new_image(3),
mlx_loop(3)

# AUTHOR

Copyright ol@ - 2002-2025 - Olivier Crouzet
