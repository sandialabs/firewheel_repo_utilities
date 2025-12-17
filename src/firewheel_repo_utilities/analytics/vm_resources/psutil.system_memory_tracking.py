import sys
import logging
from time import sleep

import psutil
from json_logger import JSONLogger


# pylint: disable=consider-using-f-string
class SystemMemoryTracking:
    """Track the system memory using psutil."""

    def __init__(self, refresh_interval_sec):
        """Set up the logging system and take in the refresh rate.

        Args:
            refresh_interval_sec (int): Interval between tracking the statistics.
        """
        self.refresh_interval_sec = refresh_interval_sec
        logger = logging.getLogger("system_memory_tracking")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")

        # Add logging to stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Wrap the new json logger
        self._log = JSONLogger(logger)

        logger = logging.getLogger("system_memory_tracking2")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")

        # Add logging to a file
        file_handler = logging.FileHandler("/opt/analytics/system_memory_tracking.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Add logging to stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Wrap the new json logger
        self._log2 = JSONLogger(logger)

    def run(self):
        """Start tracking the system memory."""
        self._log.debug("Starting system_memory_tracking")

        # Run every <interval> seconds to get memory statistic
        while True:
            mem = psutil.virtual_memory()  # Named tuple with stats

            mem_dict = {
                "analytics.system_memory_tracking.{}".format(k): v
                for k, v in mem._asdict().items()
            }
            self._log2.debug("", jarg=mem_dict)

            sleep(self.refresh_interval_sec)


if __name__ == "__main__":
    system_memory_tracking = SystemMemoryTracking(int(sys.argv[1]))
    system_memory_tracking.run()
