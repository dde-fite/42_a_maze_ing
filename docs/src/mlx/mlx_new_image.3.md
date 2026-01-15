# NAME

MiniLibX - Manipulating images

# SYNOPSYS

    void *

**mlx_new_image** ( *void \*mlx_ptr, unsigned int width, unsigned int
height* );

    unsigned char *

**mlx_get_data_addr** ( *void \*img_ptr, unsigned int \*bits_per_pixel,
unsigned int \*size_line, unsigned int \*format* );

    int

**mlx_put_image_to_window** ( *void \*mlx_ptr, void \*win_ptr, void
\*img_ptr, int x, int y* );

    void *

**mlx_xpm_to_image** ( *void \*mlx_ptr, const char \*\*xpm_data,
unsigned int \*width, unsigned int \*height* );

    void *

**mlx_xpm_file_to_image** ( *void \*mlx_ptr, const char \*filename,
unsigned int \*width, unsigned int \*height* );

    void *

**mlx_png_file_to_image** ( *void \*mlx_ptr, const char \*filename,
unsigned int \*width, unsigned int \*height* );

    int

**mlx_destroy_image** ( *void \*mlx_ptr, void \*img_ptr* );

# DESCRIPTION

**mlx_new_image** () creates a new image in memory. It returns a *void
\** identifier needed to manipulate this image later. It only needs the
size of the image to be created, using the *width* and *height*
parameters, and the *mlx_ptr* connection identifier (see the **mlx**
manual).

The user can draw inside the image (see below), and can dump the image
inside a specified window at any time to display it on the screen. This
is done using **mlx_put_image_to_window** (). Three identifiers are
needed here, for the connection to the display, the window to use, and
the image (respectively *mlx_ptr* , *win_ptr* and *img_ptr* ). The ( *x*
, *y* ) coordinates define where the image should be placed in the
window.

**mlx_get_data_addr** () returns information about the created image,
allowing a user to modify it later. The *img_ptr* parameter specifies
the image to use. The three next parameters should be the addresses of
three different valid unsigned integers. *bits_per_pixel* will be filled
with the number of bits needed to represent a pixel colour (also called
the depth of the image). *size_line* is the number of bytes used to
store one line of the image in memory. This information is needed to
move from one line to another in the image. *format* tells you how each
pixel colour in the image is structured. Currently only 2 values are
defined:

0 means format B8G8R8A8

1 means format A8R8G8B8

**mlx_get_data_addr** returns an *unsigned char \** address that
represents the beginning of the memory area where the image is stored.
From this address, the first *bits_per_pixel* bits represent the colour
of the first pixel in the first line of the image. The second group of
*bits_per_pixel* bits represent the second pixel of the first line, and
so on. Add *size_line* to the address to get the beginning of the second
line. You can reach any pixels of the image that way.

**mlx_destroy_image** destroys the given image ( *img_ptr* ).

# STORING COLOURS INSIDE IMAGES

Depending on the graphic system, the number of bits used to store a
pixel colour used to be different from one hardware to another. Today,
the way the user usually represents a colour, in the ARGB mode, almost
always matches the hardware capabilities on modern computers.

Keep in mind that packing the 4-byte ARGB into an unsigned int depends
on the local computer\'s endian. Adjust your code accordingly.

# XPM AND PNG IMAGES

The **mlx_xpm_to_image** () , **mlx_xpm_file_to_image** () and
**mlx_png_file_to_image** () functions will create a new image the same
way. They will fill it using the specified *xpm_data* or *filename* ,
depending on which function is used. Note that MiniLibX does not use the
standard Xpm and png libraries to deal with xpm and png images. You may
not be able to read all types of xpm and png images. It however handles
transparency.

# RETURN VALUES

The four functions that create images, **mlx_new_image()** ,
**mlx_xpm_to_image()** , **mlx_xpm_file_to_image()** and
**mlx_png_file_to_image()** , will return NULL if an error occurs.
Otherwise they return a non-null pointer as an image identifier.

# SEE ALSO

mlx(3), mlx_new_window(3), mlx_pixel_put(3), mlx_loop(3), mlx_extra(3)

# AUTHOR

Copyright ol@ - 2002-2025 - Olivier Crouzet
