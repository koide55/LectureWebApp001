import re
import subprocess


HOST_PATTERN = re.compile(r"^[A-Za-z0-9.-]+$")


def safe_ping(host):
    if not host or not HOST_PATTERN.fullmatch(host):
        return False, "Invalid host."

    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )
    return result.returncode == 0, result.stdout or result.stderr


def unsafe_ping(host):
    command = f"ping -c 1 {host}"
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=5,
        shell=True,
        check=False,
    )
    return result.returncode == 0, result.stdout or result.stderr, command
