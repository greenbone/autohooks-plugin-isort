# Copyright (C) 2019-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .isort import precommit as precommit

"""
A module containing classes and functions mostly useful for creating unit tests
"""

import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import (
    # Any,
    AsyncIterator,
    # Awaitable,
    Generator,
    # Iterable,
    # Optional,
    # Union,
)

from pontos.git._git import exec_git
from pontos.helper import add_sys_path, ensure_unload_module, unload_module

__all__ = (
    "AsyncIteratorMock",
    "add_sys_path",
    "ensure_unload_module",
    "temp_directory",
    "temp_file",
    "temp_git_repository",
    "temp_python_module",
    "unload_module",
)


@contextmanager
def temp_directory(
    *, change_into: bool = False, add_to_sys_path: bool = False
) -> Generator[Path, None, None]:
    """
    Context Manager to create a temporary directory

    Args:
        change_into: Set the created temporary as the current working directory.
            The behavior of the current working directory when leaving the
            context manager is undefined.
        add_to_sys_path: Add the created temporary directory to the directories
            for searching for Python modules

    Returns:
        A path to the created temporary directory

    Example:
        .. code-block:: python

            from pontos.testing import temp_directory

            with temp_directory(change_into=True) as tmp:
                new_file = tmp / "test.txt"
    """
    temp_dir = tempfile.TemporaryDirectory()
    dir_path = Path(temp_dir.name)

    if change_into:
        try:
            old_cwd = Path.cwd()
        except FileNotFoundError:
            old_cwd = Path.home()

        os.chdir(dir_path)

    try:
        if add_to_sys_path:
            with add_sys_path(dir_path):
                yield Path(dir_path)
        else:
            yield Path(dir_path)
    finally:
        if change_into:
            try:
                os.chdir(old_cwd)
            finally:
                temp_dir.cleanup()
        else:
            temp_dir.cleanup()

