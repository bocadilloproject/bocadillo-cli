def test_invoke(cli, runner):
    r = runner.invoke(cli)
    assert r.exit_code == 0
