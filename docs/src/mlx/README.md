---
title: MiniLibX Python Wrapper Manual
abstract: >
  This documentation is a PORT of the ORIGINAL MiniLibX docs.

  It describes the Python package that provides access to the
  MiniLibX graphics library. It allows creating windows, drawing pixels,
  handling images, and capturing keyboard and mouse input through a thin
  wrapper over the original C API, keeping function names and behavior as
  close as possible to the native MiniLibX library.
---

# Introduction

The MiniLibX Python Wrapper allows you to create graphical software easily without any knowledge of X-Window/Wayland/Vulkan on Unix/Linux, or AppKit on macOS. It provides:

- Window creation and management
- Pixel-level drawing
- Image manipulation for faster rendering
- Keyboard and mouse input handling
- PNG and XPM image loading

## How a graphics server works

This library interacts with the underlying graphics system of your operating system. Before diving into usage, it's helpful to understand how graphics servers manage windows and handle user input.


### Historical X-Window concept

X-Window is a network-oriented graphical system for Unix. It is based on two main parts:

- On one side, your software wants to draw something on the screen and or get keyboard & mouse entries.

- On the other side, the X-Server manages the screen, keyboard and mouse
(It is often referred to as a \"display\").

A network connection must be established between these two entities to
send drawing orders (from the software to the X-Server), and
keyboard/mouse events (from the X-Server to the software).

Nowadays, most of the time, both run on the same computer.

### Modern graphical approach

Modern computers come with a powerful GPU that is directly accessed by
applications. Along GPU libraries like Vulkan or OpenGL, the Wayland
protocol ensure communication with the compositor program that manages
the various windows on screen and the user input events. For your own
application:

- The Vulkan or OpenGL library allow you to directly draw any content into
your window.
- The Wayland compositor handles the place of your window on screen and
send you back the keyboard and mouse inputs from the user.

Unfortunately, this gain of graphical power through GPU access removes
the networking aspects that exist with X-Window. It is not possible for
a program to access a remote GPU and show its window on a remote
display. But current software architectures are more likely based on a
local display application that gets data in JSON through a web API.

# Getting Started

## Requirements
### Arch Linux
```bash
sudo pacman -S libxcb xcb-util-keysyms zlib libbsd vulkan-icd-loader vulkan-tools shaderc
```

### Debian/Ubuntu
```bash
sudo apt install libxcb libxcb-keysyms libvulkan libz libbsd glslc
```

## Installation
First compile MiniLibX.
```bash
make install
```

Create a virtual environment with your preferred manager and open it:

- For bash/zsh:
```bash
python -m venv .venv
source .venv/bin/activate
```

- For fish:
```bash
python -m venv .venv
source .venv/bin/activate.fish
```

And install the package:
```bash
pip install mlx_CLXV-2.2-py3-none-any.whl
```

## Example of use

This small Python script displays a small black window with text. It will also print the screen dimensions to stdout and listen for user clicks.

We will explain the functions used in this example later.

```python
from mlx import Mlx

def mymouse(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at {x},{y}.")

def mykey(keynum, mystuff):
    print(f"Got key {keynum}, and got my stuff back:")
    print(mystuff)
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)

m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 200, 200, "test")
m.mlx_clear_window(mlx_ptr, win_ptr)
m.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
(ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
print(f"Got screen size: {w} x {h} .")

stuff = [1, 2]
m.mlx_mouse_hook(win_ptr, mymouse, None)
m.mlx_key_hook(win_ptr, mykey, stuff)

m.mlx_loop(mlx_ptr)
```

# Behind the Scenes

When an instance of the Mlx class is created, the first thing it does is construct the path to the C library called libmlx.so.

```python
def __init__(self):
  module_dir = os.path.dirname(os.path.abspath(__file__))
  self.so_file = os.path.join(module_dir, "libmlx.so")
  #...
```

- \_\_file\_\_ is a special Python variable that contains the path to the file where this code is executed.

- os.path.dirname extracts the path from __file__ and uses os.path.join to create the path to the library.

It then declares the mlx_func variable, which acts as a bridge between Python and C. Using the CDLL function from Python's ctypes module, it loads the library and calls the original functions.

```python
def __init__(self):
  # ...
  self.mlx_func = CDLL(self.so_file)
  # ...
```

For each C function available in the Python wrapper, there is a declaration within the Mlx class:

```python
def mlx_init(self):
  self.mlx_func.mlx_init.restype = c_void_p
  return self.mlx_func.mlx_init()
```

You can see how it calls mlx_func.mlx_init(). This mlx_init() is already the original C function. It is necessary to specify the data type returned by the function with mlx_init.restype, which in this case is c_void_p (equivalent to void *).

All of this is passed to CDLL, which, using the previously loaded library, will execute the function and return whatever the function returns.


# Initialization and Cleanup: mlx_init() and mlx_release()

## Synopsis

```python
from mlx import Mlx

def mlx_init() -> int # void *

def mlx_release() -> int # void *
```

## Description

First of all, you need to initialize the connection between your software and the graphic and user sub-systems. Once this completed, you'll be able to use other MiniLibX functions to send and receive the messages from the display, like "I want to draw a yellow pixel in this window" or "did the user hit a key?".

The mlx_init function will create this connection. No parameters are needed, ant it will return a void * identifier, used for further calls to the library routines. The mlx_release function can be used at the end of the program to disconnect from the graphic system and release resources.

If **mlx_init()** fails to set up the connection to the display, it will return NULL, otherwise a non-null pointer is returned as a connection identifier.
