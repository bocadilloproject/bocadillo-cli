def test_invoke(cli, runner):
    r = runner.invoke(cli)
    assert r.exit_code == 0


# TODO: test project generation
# TODO: test --dry mode
# TODO: test skipping existing files
# TODO: test --no-input mode
