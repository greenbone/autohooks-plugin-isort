# Copyright (C) 2020 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from pontos.testing import temp_git_repository

from autohooks.api.git import StatusEntry
from autohooks.config import load_config_from_pyproject_toml
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
        CONTENT: str = (  # noqa: I001
            """
# pylint: disable-all
from io import StringIO, BytesIO, FileIO  # pylint: disable=unused-import
import sys
import black

import autohooks

cmd = ["pylint", "autohooks/pluginrecommit_stages/pylint/pylint.py"]
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
        )
        with temp_git_repository() as temp_dir:
            test_file = temp_dir / "test.py"
            test_file.write_text(data=CONTENT, encoding="utf8")
            staged_mock.return_value = [StatusEntry(f"M  {test_file}")]
            ret = precommit()
            self.assertFalse(ret)
