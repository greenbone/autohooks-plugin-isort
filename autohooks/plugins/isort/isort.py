# Copyright (C) 2019-2022 Greenbone Networks GmbH
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

from autohooks.api import out, ok, error
from autohooks.api.git import (
    get_staged_status,
    stage_files_from_status_list,
    stash_unstaged_changes,
)
from autohooks.api.path import match

DEFAULT_INCLUDE = ('*.py',)


def check_isort_installed():
    try:
        import isort  # pylint: disable=unused-import, import-outside-toplevel
    except ImportError:
        raise Exception(
            'Could not find isort. Please add isort to your python environment'
        ) from None


def get_isort_config(config):
    return config.get('tool', 'autohooks', 'plugins', 'isort')


def get_include_from_config(config):
    if not config:
        return DEFAULT_INCLUDE

    isort_config = get_isort_config(config)
    include = isort_config.get_value('include', DEFAULT_INCLUDE)

    if isinstance(include, str):
        return [include]

    return include


def precommit(config=None, **kwargs):  # pylint: disable=unused-argument
    out('Running isort pre-commit hook')

    check_isort_installed()

    include = get_include_from_config(config)
    files = [f for f in get_staged_status() if match(f.path, include)]

    if len(files) == 0:
        ok('No staged files for isort available')
        return 0

    with stash_unstaged_changes(files):
        for f in files:
            try:
                subprocess.check_call(['isort', '-q', str(f.absolute_path())])
                ok(f'Running isort on {str(f.path)}')
            except subprocess.CalledProcessError as e:
                error(f'Running isort on {str(f.path)}')
                raise e

        stage_files_from_status_list(files)

    return 0
