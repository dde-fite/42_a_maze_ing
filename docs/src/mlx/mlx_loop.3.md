# NAME

MiniLibX - Handle events

# SYNOPSYS

    int

**mlx_loop** ( *void \*mlx_ptr* );

    int

**mlx_key_hook** ( *void \*win_ptr, int (\*funct_ptr)(), void \*param*
);

    int

**mlx_mouse_hook** ( *void \*win_ptr, int (\*funct_ptr)(), void \*param*
);

    int

**mlx_expose_hook** ( *void \*win_ptr, int (\*funct_ptr)(), void
\*param* );

    int

**mlx_loop_hook** ( *void \*mlx_ptr, int (\*funct_ptr)(), void \*param*
);

    int

**mlx_loop_exit** ( *void \*mlx_ptr* );

# EVENTS

The graphical system is bi-directional. On one hand, the program sends
orders to the screen to display pixels, images, and so on. On the other
hand, it can get information from the keyboard and mouse associated to
the screen. To do so, the program receives \"events\" from the keyboard
or the mouse.

# DESCRIPTION

To receive events, you must use **mlx_loop** (). This function never
returns, unless **mlx_loop_exit** is called. It is an infinite loop that
waits for an event, and then calls a user-defined function associated
with this event. A single parameter is needed, the connection identifier
*mlx_ptr* (see the **mlx manual).**

You can assign different functions to the three following events:\
- A key is released\
- The mouse button is pressed\
- A part of the window should be re-drawn (this is called an \"expose\"
event, and it is your program\'s job to handle it in the Unix/Linux X11
environment, but at the opposite it never happens on Unix/Linux
Wayland-Vulkan nor on MacOS).\

Each window can define a different function for the same event.

The three functions **mlx_key_hook** (), **mlx_mouse_hook** () and
**mlx_expose_hook** () work exactly the same way. *funct_ptr* is a
pointer to the function you want to be called when an event occurs. This
assignment is specific to the window defined by the *win_ptr*
identifier. The *param* address will be passed back to your function
every time it is called, and should be used to store the parameters it
might need.

The syntax for the **mlx_loop_hook** () function is similar to the
previous ones, but the given function will be called when no event
occurs, and is not bound to a specific window.

When it catches an event, the MiniLibX calls the corresponding function
with fixed parameters:


      expose_hook(void *param);
      key_hook(unsigned int keycode, void *param);
      mouse_hook(unsigned int button, unsigned int x, unsigned int y, void *param);
      loop_hook(void *param);

These function names are arbitrary. They here are used to distinguish
parameters according to the event. These functions are NOT part of the
MiniLibX.

*param* is the address specified in the mlx\_\*\_hook calls. This
address is never used nor modified by the MiniLibX. On key and mouse
events, additional information is passed: *keycode* tells you which key
is pressed (just try to find out :) ), ( *x* , *y* ) are the coordinates
of the mouse click in the window, and *button* tells you which mouse
button was pressed.

# GOING FURTHER WITH EVENTS

The MiniLibX provides a much generic access to other available events.
The *mlx.h* include define **mlx_hook()** in the same manner
mlx\_\*\_hook functions work. The event and mask values will be taken
from the historical X11 include file \"X.h\". Some Wayland and MacOS
events are mapped to these values when it makes sense, and the mask may
not be used in some configurations.

See source code of the MiniLibX to find out how it will call your own
function for a specific event.

# SEE ALSO

mlx(3), mlx_new_window(3), mlx_pixel_put(3), mlx_new_image(3),
mlx_extra(3)

# AUTHOR

Copyright ol@ - 2002-2025 - Olivier Crouzet
