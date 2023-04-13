from .context import app

from typer.testing import CliRunner

runner = CliRunner()

def test_main_help():
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0
    arguments = ['repos']
    for argument in arguments:
        assert argument in result.stdout

def test_repos_help():
    result = runner.invoke(app, ['repos', '--help'])
    assert result.exit_code == 0
    arguments = ['add']
    for argument in arguments:
        assert argument in result.stdout

