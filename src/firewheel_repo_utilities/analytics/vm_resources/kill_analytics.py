#!/usr/bin/env python3
import sys
import logging
import subprocess

from pythonjsonlogger.json import JsonFormatter

# pylint: disable=consider-using-f-string

self._log = logging.getLogger("kill_analytics")
self._log.setLevel(logging.DEBUG)
formatter = JsonFormatter()

# Add logging to stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
self._log.addHandler(console_handler)


def kill_all():
    """A function to kill any running analytics scripts."""
    possible_processes = [
        "tcpdump",
        "analytics.port_tracking.py",
        "analytics.strace.py",
        "strace",
        "analytics.tailf_dir.sh",
        "tail -f",
        "psutil.cpu_tracking.py",
        "psutil.disk_io_tracking.py",
        "psutil.disk_usage_tracking.py",
        "psutil.network_io_tracking.py",
        "psutil.system_memory_tracking.py",
    ]

    for process_regex in possible_processes:
        try:
            subprocess.run(["pkill", "-f", "{}".format(process_regex)], check=True)
        except subprocess.CalledProcessError:
            pass
        else:
            log.debug(
                "Sent SIGTERM to at least one process matching '%s'", process_regex
            )


if __name__ == "__main__":
    kill_all()
