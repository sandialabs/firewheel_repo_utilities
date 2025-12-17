import sys
import json
import logging
import datetime
from time import sleep

import psutil
from json_logger import JSONLogger


# pylint: disable=consider-using-f-string,unspecified-encoding
class CPUTracking:
    """Track the system CPU usage using psutil."""

    def __init__(self, refresh_interval_sec):
        """Set up the logging system and take in the refresh rate.

        Args:
            refresh_interval_sec (int): Interval between tracking the statistics.
        """
        self.refresh_interval_sec = refresh_interval_sec
        logger = logging.getLogger("cpu_tracking")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")

        # Add logging to stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Wrap the new json logger
        self._log = JSONLogger(logger)

    def run(self):
        """Start tracking the system CPU."""
        self._log.debug("Starting cpu_tracking")

        with open("/opt/analytics/cpu_tracking.log", "a", encoding="utf-8") as outfile:
            # Run every <interval> seconds to get memory statistic
            while True:
                cpu_percents = psutil.cpu_percent(
                    percpu=True
                )  # List of named tuples with stats

                cpu_dict = {
                    "date": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
                }

                for cpu, cpu_percent in enumerate(cpu_percents):
                    cpu_dict["cpu{}".format(cpu)] = cpu_percent

                outfile.write("{}\n".format(json.dumps(cpu_dict)))
                outfile.flush()

                sleep(self.refresh_interval_sec)


if __name__ == "__main__":
    cpu_tracking = CPUTracking(int(sys.argv[1]))
    cpu_tracking.run()
