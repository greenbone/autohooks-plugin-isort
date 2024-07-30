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

import subprocess
from typing import Iterable, List, Optional, Union

from autohooks.api import error, ok
from autohooks.api.git import (
    get_staged_status,
    stage_files_from_status_list,
    stash_unstaged_changes,
)
from autohooks.api.path import match
from autohooks.config import Config
from autohooks.precommit.run import ReportProgress

DEFAULT_INCLUDE = ("*.py",)
DEFAULT_ARGUMENTS = ("-q",)
CONTENT = """
# pylint: disable-all
from io import StringIO, BytesIO, FileIO  # pylint: disable=unused-import
import sys
import black

import autohooks

cmd = ["pylint", "autohooks/plugins/pylint/pylint.py"]
import subprocess  # pylint: disable=

# status = subprocess.call(cmd)
iofile = "tmp.txt"
# status = subprocess.call(cmd, stdout=iofile)
# blah blah lots of code ...

status = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = status.communicate()
print(out.decode(encoding="utf-8"))
print(err.decode(encoding="utf-8"))
"""


def check_isort_installed() -> None:
    try:
        import isort
    except ImportError:
        raise Exception(
            "Could not find isort. Please add isort to your python environment"
        ) from None


def get_isort_config(config: Config) -> Config:
    return config.get("tool", "autohooks", "plugins", "isort")


def ensure_iterable(value: Union[List[str], str]) -> List[str]:
    if isinstance(value, str):
        return [value]
    return value


def get_include_from_config(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_INCLUDE

    isort_config = get_isort_config(config)
    return ensure_iterable(isort_config.get_value("include", DEFAULT_INCLUDE))


def get_isort_arguments(config: Optional[Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_ARGUMENTS

    isort_config = get_isort_config(config)
    return ensure_iterable(
        isort_config.get_value("arguments", DEFAULT_ARGUMENTS)
    )


def precommit(
    config: Optional[Config] = None,
    report_progress: Optional[ReportProgress] = None,
    **kwargs,
) -> int:
    check_isort_installed()

    include = get_include_from_config(config)
    files = [f for f in get_staged_status() if match(f.path, include)]

    if len(files) == 0:
        ok("No staged files for isort available")
        return 0

    if report_progress:
        report_progress.init(len(files))

    arguments = ["isort"]
    arguments.extend(get_isort_arguments(config))

    with stash_unstaged_changes(files):
        for f in files:
            try:
                args = arguments.copy()
                args.append(str(f.absolute_path()))

                subprocess.check_call(args)
                ok(f"Running isort on {str(f.path)}")
                if report_progress:
                    report_progress.update()
            except subprocess.CalledProcessError as e:
                error(f"Running isort on {str(f.path)}")
                raise e from None

        stage_files_from_status_list(files)

    return 0
