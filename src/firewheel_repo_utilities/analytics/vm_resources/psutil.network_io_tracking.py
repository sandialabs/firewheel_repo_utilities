import sys
import logging
from time import sleep

import psutil
from json_logger import JSONLogger


# pylint: disable=consider-using-f-string
class NetworkIOTracking:
    """Track the network IO rate using psutil."""

    def __init__(self, refresh_interval_sec):
        """Set up the logging system and take in the refresh rate.

        Args:
            refresh_interval_sec (int): Interval between tracking the statistics.
        """
        self.refresh_interval_sec = refresh_interval_sec
        logger = logging.getLogger("network_io_tracking")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")

        # Add logging to stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Wrap the new json logger
        self._log = JSONLogger(logger)

        logger = logging.getLogger("network_io_tracking2")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")

        # Add logging to a file
        file_handler = logging.FileHandler("/opt/analytics/network_io_tracking.log")
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
        """Start tracking the network IO."""
        self._log.debug("Starting network_io_tracking")

        nics = psutil.net_if_addrs()

        # Run every <interval> seconds
        while True:
            # Get the IO stats for each nic
            compiled_stats = {}
            io_counters = psutil.net_io_counters(pernic=True)
            for nic in nics.keys():
                if nic in io_counters:
                    io_tupe = io_counters[nic]  # Named tuple with stats
                    compiled_stats["analytics.network_io_tracking.{}".format(nic)] = (
                        io_tupe._asdict()
                    )
            self._log2.debug("", jarg=compiled_stats)

            sleep(self.refresh_interval_sec)


if __name__ == "__main__":
    network_io_tracking = NetworkIOTracking(int(sys.argv[1]))
    network_io_tracking.run()
