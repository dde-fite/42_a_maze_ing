# NAME

MiniLibX - Simple Window Interface Library for students

# SYNOPSYS

#include \<mlx.h\>

    void *

**mlx_init** ();

    int

**mlx_release** (void \*mlx_ptr);

# DESCRIPTION

MiniLibX is an easy way to create graphical software, without any
X-Window/Wayland/Vulkan programming knowledge under Unix/Linux, nor any
AppKit programming knowledge under MacOS. It provides simple window
creation, a drawing tool, image and basic events management.

# Unix/Linux: HISTORICAL X-WINDOW CONCEPT

X-Window is a network-oriented graphical system for Unix. It is based on
two main parts:\
On one side, your software wants to draw something on the screen and/or
get keyboard & mouse entries.\
On the other side, the X-Server manages the screen, keyboard and mouse
(It is often referred to as a \"display\").\
A network connection must be established between these two entities to
send drawing orders (from the software to the X-Server), and
keyboard/mouse events (from the X-Server to the software).\
Nowadays, most of the time, both run on the same computer.

# Unix/Linux: MODERN GRAPHICAL APPROACH

Modern computers come with a powerful GPU that is directly accessed by
applications. Along GPU libraries like Vulkan or OpenGL, the Wayland
protocol ensure communication with the compositor program that manages
the various windows on screen and the user input events. For your own
application:\
The Vulkan or OpenGL library allow you to directly draw any content into
your window.\
The Wayland compositor handles the place of your window on screen and
send you back the keyboard and mouse inputs from the user.\
Unfortunately, this gain of graphical power through GPU access removes
the networking aspects that exist with X-Window. It is not possible for
a program to access a remote GPU and show its window on a remote
display. But current software architectures are more likely based on a
local display application that gets data in JSON through a web API.

# MacOS: WINDOW SERVER AND GPU

Your software interacts directly with the Window server who handles the
cohabitation on the screen with other software and the event system, and
interacts with the GPU to handle all drawing commands.

# INCLUDE FILE

**mlx.h** should be included for a correct use of the MiniLibX API. It
only contains function prototypes, no structure is needed.

# LIBRARY FUNCTIONS

First of all, you need to initialize the connection between your
software and the graphic and user sub-systems. Once this completed,
you\'ll be able to use other MiniLibX functions to send and receive the
messages from the display, like \"I want to draw a yellow pixel in this
window\" or \"did the user hit a key?\".

The **mlx_init** function will create this connection. No parameters are
needed, ant it will return a *void \** identifier, used for further
calls to the library routines. The **mlx_release** function can be used
at the end of the program to disconnect from the graphic system and
release resources.

All other MiniLibX functions are described in the following man pages:

**mlx_new_window**

:   : manage windows

**mlx_pixel_put**

:   : draw inside a window

**mlx_new_image**

:   : manipulate images

**mlx_loop**

:   : handle keyboard or mouse events

**mlx_extra**

:   : extra functions available in the MinilibX

# LINKING MiniLibX

To use MiniLibX functions, you may -or not- need to link your software
with several libraries, including the MiniLibX library itself. On
Unix/Linux, depending on the specific operating system, either just
using **-lmlx** works, or you need to add **-lxcb -lxcb-keysyms -lvulkan
-lz -lbsd** . On MacOS, the dynamic Metal library will find on its own
the missing components: **-lmlx** .

You may also need to specify the path to these libraries, using the
**-L** flag.

# RETURN VALUES

If **mlx_init()** fails to set up the connection to the display, it will
return NULL, otherwise a non-null pointer is returned as a connection
identifier.

# SEE ALSO

mlx_new_window(3), mlx_pixel_put(3), mlx_new_image(3), mlx_loop(3),
mlx_extra(3)

# AUTHOR

Copyright ol@ - 2002-2025 - Olivier Crouzet
