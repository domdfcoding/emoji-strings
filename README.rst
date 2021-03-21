##############
emoji-strings
##############

.. start short_desc

**Adds support for emoji-strings in Python, which convert emoji names into actual emoji.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/domdfcoding/emoji-strings/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/emoji-strings/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/emoji-strings/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/emoji-strings/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/emoji-strings/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/emoji-strings/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/emoji-strings/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/emoji-strings/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/emoji-strings/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/emoji-strings/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/domdfcoding/emoji-strings/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/emoji-strings/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/emoji-strings/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/emoji-strings?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/emoji-strings?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/emoji-strings
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/emoji-strings
	:target: https://pypi.org/project/emoji-strings/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/emoji-strings?logo=python&logoColor=white
	:target: https://pypi.org/project/emoji-strings/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/emoji-strings
	:target: https://pypi.org/project/emoji-strings/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/emoji-strings
	:target: https://pypi.org/project/emoji-strings/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/emoji-strings
	:target: https://github.com/domdfcoding/emoji-strings/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/emoji-strings
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/emoji-strings/v0.1.0
	:target: https://github.com/domdfcoding/emoji-strings/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/emoji-strings
	:target: https://github.com/domdfcoding/emoji-strings/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/emoji-strings
	:target: https://pypi.org/project/emoji-strings/
	:alt: PyPI - Downloads

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/emoji-strings/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/emoji-strings/master
	:alt: pre-commit.ci status

.. end shields

Installation
--------------

.. start installation

``emoji-strings`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install emoji-strings

.. end installation

Usage
---------

Emoji strings (g-strings for short) are similar to Python's f-strings.
However, rather than using curly braces, g-strings use colons to mark emoji in a string.
For example, in the following sentence, ``:rocket:`` denotes a substitution, in this case for a 🚀 emoji:

	Deploy the app :rocket:

In a Python source file, you can write this as:

.. code-block:: python

	print(g"Deploy the app :rocket:")
	#     ^ note the "g" prefix character

which would print::

	Deploy the app 🚀

Ta da! You no longer need to remember unicode code points or use cumbersome emoji entry dialogs.
To enable this magic, add the following comment to the top of your python source file::

	# -*- coding: emoji_strings -*-

and add ``emoji-strings`` to your ``requirements.txt`` file.

Disclaimer
------------

This is a joke.

While this absolutely does work I made it for fun.
Someone had asked me if, since Python has f-strings, it also has g-strings?
It does now.

Credits
----------

Based on `future-fstrings <https://pypi.org/project/future-fstrings/>`_,
and uses the `emoji library <https://pypi.org/project/emoji/>`_ to parse the emoji names.
