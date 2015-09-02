__author__ = 'alonsobarquero'

import subprocess


def execute_cli_command(commands):
    """
    Execute cli commands and print the output in terminal
    :param commands: list of command lines to execute in a list object
    :return:
    """
    try:
        cmd = ""
        for command in commands:
            cmd += str("{};".format(command))
        process = subprocess.Popen(cmd, shell=True)
        process.communicate()
        output = process.communicate()[0]
        exit_code = process.returncode

        if exit_code != 0:
            raise Exception(command, exit_code, output)
        return output
    except Exception, e:
        print e.message
execute_cli_command(["locust -f locustfile.py -c 250 -r 250 --no-web --only-summary"])
