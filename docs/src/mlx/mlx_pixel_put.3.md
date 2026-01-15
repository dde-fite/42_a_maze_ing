# NAME

MiniLibX - Drawing inside windows

# SYNOPSYS

    int

**mlx_pixel_put** ( *void \*mlx_ptr, void \*win_ptr, unsigned int x,
unsigned int y, unsigned int color* );

    int

**mlx_string_put** ( *void \*mlx_ptr, void \*win_ptr, unsigned int x,
unsigned int y, unsigned int color, char \*string* );

# DESCRIPTION

The **mlx_pixel_put** () function draws a defined pixel in the window
*win_ptr* using the ( *x* , *y* ) coordinates, and the specified *color*
. The origin (0,0) is the upper left corner of the window, the x and y
axis respectively pointing right and down. The connection identifier,
*mlx_ptr* , is needed (see the **mlx** man page).

Parameters for **mlx_string_put** () have the same meaning. Instead of a
simple pixel, the specified *string* will be displayed at ( *x* , *y* ).

Both functions will discard any display outside the window. This makes
**mlx_pixel_put** slow. Consider using images instead.

# COLOUR MANAGEMENT

The *color* parameter has an unsigned integer type. The displayed colour
needs to be encoded in this integer, following a defined scheme. All
displayable colours can be split in 3 basic colours: red, green and
blue. Three associated values, in the 0-255 range, represent how much of
each colour is mixed up to create the original colour. The fourth byte
represent transparency, where 0 is fully transparent and 255 opaque.
Theses four values must be set inside the unsigned integer to display
the right colour. The bytes of this integer are filled as shown in the
picture below:

            | B | G | R | A |   colour integer
            +---+---+---+---+

While filling the integer, make sure you avoid endian problems. Example:
the \"blue\" byte will be the least significant byte inside the integer
on a little endian machine.

# SEE ALSO

mlx(3), mlx_new_window(3), mlx_new_image(3), mlx_loop(3), mlx_extra(3)

# AUTHOR

Copyright ol@ - 2002-2025 - Olivier Crouzet
