import sys
import logging
from time import sleep

import psutil
from json_logger import JSONLogger


# pylint: disable=consider-using-f-string
class DiskIOTracking:
    """Track the system disk IO."""

    def __init__(self, refresh_interval_sec):
        """Set up the logging system and take in the refresh rate.

        Args:
            refresh_interval_sec (int): Interval between tracking the statistics.
        """
        self.refresh_interval_sec = refresh_interval_sec
        logger = logging.getLogger("disk_io_tracking")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")

        # Add logging to stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Wrap the new json logger
        self._log = JSONLogger(logger)

        logger = logging.getLogger("disk_io_tracking2")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")

        # Add logging to a file
        file_handler = logging.FileHandler("/opt/analytics/disk_io_tracking.log")
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
        """Start tracking the system disk IO."""
        self._log.debug("Starting disk_io_tracking")

        # Run every <interval> seconds to get memory statistic
        while True:
            # Get the usage statistics for each disk partition
            disk_io_stats = {}
            for partition, stats in psutil.disk_io_counters(perdisk=True).items():
                disk_io_stats["analytics.disk_io_tracking.{}".format(partition)] = (
                    stats._asdict()
                )
            self._log2.debug("", jarg=disk_io_stats)

            sleep(self.refresh_interval_sec)


if __name__ == "__main__":
    disk_io_tracking = DiskIOTracking(int(sys.argv[1]))
    disk_io_tracking.run()
