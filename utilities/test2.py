from custom_runner import custom_runner

custom_runner.execute_cli_command(["source env/bin/activate", "pip freeze -l"])
