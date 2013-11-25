cookiejar
===============
Cookiecutter templates discovery and management.

NOTE: This project requires https://github.com/audreyr/cookiecutter/pull/75 to be merged in cookiecutter.

Usage::

    $ pip install cookiejar
    $ cookiejar create <templatename> [options]

Will use `cookiecutter <https://github.com/audreyr/cookiecutter>`_ to create a new package from the template.

Options
=======
All options can be specified on the command-line. Users can override everything by creating a config file at ``~/.cookiejar/cookiejarrc``.

Managing templates
==================
You can list, search and download templates from a 'templates index'.

The following commands are available::

    $ cookiejar list [--index=<index>]
    $ cookiejar search <text> [--index=<index>]
    $ cookiejar add <package_name> [<url>] [--index=<index>]
    $ cookiejar installed
    $ cookiejar remove <package_name>

Creating new packages from a template
=====================================
To create a new package::

    $ cookiejar create <template_name> [options]

Available Commands
==================

``list``
^^^^^^^^
Lists all templates available on the index.

Options
-------

``--index=<url>``
~~~~~~~~~~~~~~~~~
Optional. Specifies an alternative index to use.

``search``
^^^^^^^^^^
Lists available templates on the index whose name contains the specified text.

Options
-------

``<text>``
~~~~~~~~~~
Required. Text to look for in the index.

``--index=<url>``
~~~~~~~~~~~~~~~~~
Optional. Specifies an alternative index to use.

``add``
^^^^^^^
Downloads the specified template to your ``~/.cookiecutters/templates/`` directory.

Options
-------

``<template_name>``
~~~~~~~~~~~~~~~~~~~
Required. The template you want to download.

``<url>``
~~~~~~~~~
Optional. If specified, downloads the template from there instead of using the index. Accepts ``pip``-like URLs, as ``git+https://github.com/user/repo.git``.

``--index=<url>``
~~~~~~~~~~~~~~~~~
Optional. Specifies an alternative index to use.

``installed``
^^^^^^^^^^^^^
Lists templates that have already been downloaded.

``remove``
^^^^^^^^^^
Deletes the specified template from your ``~/.cookiecutters/templates/`` directory.

Options
-------

``<template_name>``
~~~~~~~~~~~~~~~~~~~
Required. The template you want to remove.

``create``
^^^^^^^^^^
Creates a new package using the specified template.

Options
-------

``<template_name>``
~~~~~~~~~~~~~~~~~~~
Required. The template you to use.

``[options]``
~~~~~~~~~~~~~
Optional. Any options specified will be added to cookiecutter's context when creating the package. Options are specified as ``--key=value``.

TODO
====

* add ``register`` and ``upload`` commands
* use an actual REST API and server (requires $$ for the infrastructure)
* put a pretty picture of a cookie jar in this readme.

Status
======
This software should be considered Alpha.

License
=======
This project is released under the MIT License.
