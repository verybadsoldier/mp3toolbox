"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = mp3toolbox.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import os
from pathlib import Path
import sys

from mp3toolbox import __version__
from mp3toolbox.modes import groom_genres, remove_double_albumartist, title_to_album

__author__ = "verybadsoldier"
__copyright__ = "verybadsoldier"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version=f"mp3toolbox {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    parser.add_argument(
        "input_folder",
        help="root directoy with media files",
        type=str,
    )

    subparsers = parser.add_subparsers()

    for mode in (groom_genres, remove_double_albumartist, title_to_album):
        name = mode.__name__.split(".")[-1]
        mode_parser = subparsers.add_parser(name)
        mode_parser.set_defaults(func=mode.process)
    # groom_albumartist = subparsers.add_parser("groom_albumartist")
    # groom_albumartist.set_defaults(sdf="grrom_albumartist")
    #
    # genre_sanitize = subparsers.add_parser("genre_sanitize")
    # genre_sanitize.set_defaults(sdf="genre_sanitize")

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")

    for subdir, dirs, files in os.walk(args.input_folder):
        for file in files:
            fullpath = Path(subdir + "/" + file)
            if fullpath.suffix not in [".mp3", ".m4a"]:
                continue

            try:
                _logger.info(f"Processing file: {fullpath}")
                args.func(subdir, file, fullpath)
            except Exception as e:
                _logger.error(f"Error processing file: {fullpath}. Error: {str(e)}")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
