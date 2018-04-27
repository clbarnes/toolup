# toolup

Convenience package for installing python-based development tools

Supports python >=3.6.1

## Motivation

Python is a powerful and accessible language to read and write.
As such, many tools useful to developers across many languages are written in python.
However, isolation of development environments is vital, filling up your requirements
files with tools which *you* use, and your code doesn't, can be counterproductive.

However, installing things in the system python can be dangerous 
or require privileges you don't have.

If you're using python tools for python development, 
the tools and your project may have different version constraints.
For example, the opinionated code formatter `black` works on all python code, 
but can only run in version >=3.6.1.

If you're using python tools for development in other languages, 
it may not be worth the overhead of maintaining and porting separate virtual environments
just for these tools.

`toolup` helps you maintain a suite of development tools based on a simple TOML file,
which are encapsulated in a virtual environment but accessible from anywhere.

## Installation

```bash
pip install toolup
```

## Usage

### Config file

See `toolup.toml.example` for an example. 
If you keep this file in your home directory as `.toolup.toml`, 
it will be picked up automatically if `toolup` is run with no arguments.

`target` should be a directory on your path. 
If not present, and a target is not supplied at the command line, 
executables will not be linked.

Each section should be named for a tool. 
I recommend using the name as it appears on PyPI: 
this way, if `install_args` are not supplied, it can be used to find the package.

In each section, you may include `install_args` 
(a string or list of strings which will be passed directory to pip). 
This is useful for installing packages from github, or in editable mode etc..
If not given, the section name will be used.
You can also include `entry_points`; 
a list of names of entry points which this package installs. 
If not given, the section name will be used.

### Command line

```
usage: toolup [-h] [-c CONFIG] [-n NAME] [-i INSTALL_ARGS] [-e ENTRY_POINTS]
              [-t TARGET] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to config TOML file
  -n NAME, --name NAME  Name to install
  -i INSTALL_ARGS, --install_args INSTALL_ARGS
                        Arguments to pass to pip
  -e ENTRY_POINTS, --entry_points ENTRY_POINTS
                        Entry points to copy
  -t TARGET, --target TARGET
                        Where to link executables
  -f, --force           Whether to delete existing executables
```

Several entries can be added at once like so:

```bash
toolup -n black -n pgcli
```

The resulting lists of names, install_args, and entry_points are `zip_longest`'d together.
`toolup` will try to infer the install_args and entry_points from the name, 
and the name from the install_args.

### Example workflow

You've just started up a new machine.
You have a list of your favourite development tools, 
which will be useful across a few projects, 
while not actually being used by any of the code in those projects.

You copy across your `.toolup.toml` (maybe using something like GNU stow),
create a virtualenv for it, `pip install toolup && toolup`, 
and all your tools are right where you want them again.
