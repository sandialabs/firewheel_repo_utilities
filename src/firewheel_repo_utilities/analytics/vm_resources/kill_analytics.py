#!/usr/bin/env python3
import sys
import logging
import subprocess

from json_logger import JSONLogger

# pylint: disable=consider-using-f-string

logger = logging.getLogger("kill_analytics")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(message)s")

# Add logging to stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Wrap the new json logger
log = JSONLogger(logger)


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
