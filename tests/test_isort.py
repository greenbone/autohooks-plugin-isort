# Copyright (C) 2020 Greenbone Networks GmbH
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

import sys

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from autohooks.config import load_config_from_pyproject_toml
from autohooks.api.git import StatusEntry

from autohooks.plugins.isort.isort import (
    DEFAULT_ARGUMENTS,
    DEFAULT_INCLUDE,
    check_isort_installed,
    ensure_iterable,
    get_include_from_config,
    get_isort_arguments,
    get_isort_config,
    precommit,
)


def get_test_config_path(name):
    return Path(__file__).parent / name


class AutohooksIsortTestCase(TestCase):
    def test_isort_installed(self):
        sys.modules["isort"] = None
        with self.assertRaises(Exception):
            check_isort_installed()
        # pop setting module to None again for other tests
        sys.modules.pop("isort")

    def test_get_isort_arguments(self):
        args = get_isort_arguments(config=None)
        self.assertEqual(args, DEFAULT_ARGUMENTS)

    def test_get_isort_config(self):
        config_path = get_test_config_path("pyproject.test.toml")
        self.assertTrue(config_path.is_file())

        autohooksconfig = load_config_from_pyproject_toml(config_path)

        isort_config = get_isort_config(autohooksconfig.get_config())
        self.assertEqual(isort_config.get_value("foo"), "bar")

    def test_ensure_iterable(self):
        test_var = "bar"
        bar_var = ensure_iterable(test_var)
        self.assertEqual(bar_var, ["bar"])

        test_var = ["bar"]
        bar_var = ensure_iterable(test_var)
        self.assertEqual(bar_var, ["bar"])

    def test_get_include_from_config(self):
        include = get_include_from_config(config=None)
        self.assertEqual(include, DEFAULT_INCLUDE)

    @patch("autohooks.plugins.isort.isort.ok")
    def test_precommit(self, _ok_mock):
        ret = precommit()
        self.assertFalse(ret)

    # these Terminal output functions don't run in the CI ...
    @patch("autohooks.plugins.isort.isort.ok")
    @patch("autohooks.plugins.isort.isort.error")
    @patch("autohooks.plugins.isort.isort.get_staged_status")
    def test_precommit_staged(self, staged_mock, _error_mock, _ok_mock):
        staged_mock.return_value = [StatusEntry("M  tests/isort_test.py")]
        ret = precommit()
        self.assertFalse(ret)
