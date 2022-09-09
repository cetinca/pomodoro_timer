import subprocess


class CommandExecutor:
    """Creates subprocess to execute shell commands"""

    def __init__(self, cmd):
        self.cmd = cmd
        self.cmd_out = str()
        self.cmd_err = str()
        self.cmd_exc = str()
        self.__run()

    def __run(self):
        try:
            result = subprocess.run(self.cmd, shell=True, capture_output=True)
            self.cmd_out = result.stdout.decode()
            self.cmd_err = result.stderr.decode()
        except Exception as err:
            self.cmd_exc = str(err)


def notify(message):
    command = f"notify-send '{message}'"
    c = CommandExecutor(command)
    if c.cmd_exc or c.cmd_err:
        return c.cmd_exc + c.cmd_err
