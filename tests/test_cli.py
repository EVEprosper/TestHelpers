"""test_cli: make sure user experiance works as expected"""
from os import path
import tempfile
import uuid

from plumbum import local
import yaml
import plumbum
import pytest

import helpers
from testhelpers import _version
import testhelpers.RunTests as RunTests


def test_parse_command():
    """validate RunTests.parse_command behavior"""
    dummy_command = 'echo "hello world"'
    command, arguments = RunTests.parse_command(dummy_command)
    assert isinstance(command, plumbum.commands.ConcreteCommand)

    command_returns = command(arguments)
    assert command_returns.rstrip() == '"hello world"'

def test_bad_command():
    """validate RunTests.parse_command throws expected errors"""
    with pytest.raises(plumbum.commands.processes.CommandNotFound):
        command, arguments = RunTests.parse_command('garbage_command')

def test_update_coveralls():
    """validate RunTests.update_coveralls_config behavior"""
    with tempfile.TemporaryDirectory() as tempdir:
        dummy_coveralls = path.join(tempdir, '.coveralls.yml')
        dummy_token = str(uuid.uuid1())
        print(dummy_coveralls)

        # Virgin Try
        RunTests.update_coveralls_config(
            dummy_coveralls,
            dummy_token
        )

        with open(dummy_coveralls, 'r') as stream:
            coveralls_yaml = yaml.load(stream)

        assert coveralls_yaml['repo_token'] == dummy_token

        # Existing Retry
        RunTests.update_coveralls_config(
            dummy_coveralls,
            dummy_token
        )

        with open(dummy_coveralls, 'r') as stream:
            coveralls_yaml = yaml.load(stream)

        assert coveralls_yaml['repo_token'] == dummy_token

class TestCLI:
    """validate cli launches and works as users expect"""
    app_command = local['nanoci']

    def test_help(self):
        """validate -h works"""
        output = self.app_command('-h')

    def test_version(self):
        """validate app name/version are as expected"""
        output = self.app_command('--version')

        assert output.rstrip() == '{PROGNAME} {version}'.format(
            PROGNAME=_version.PROGNAME,
            version=_version.__version__,
        )
