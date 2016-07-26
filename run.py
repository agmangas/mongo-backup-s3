#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script that runs a MongoDB backup job periodically according 
to the interval defined by the INTERVAL_NAME environment variable.
"""

import schedule
import time
import datetime
import subprocess
import functools
import traceback
import os

BACKUP_SCRIPT_PATH = "/app/backup.sh"
INTERVAL_NAME = "BACKUP_INTERVAL"
INTERVAL_DEFAULT = 24


def catch_exceptions(job_func):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            job_func(*args, **kwargs)
        except:
            print(traceback.format_exc())

    return wrapper


@catch_exceptions
def backup_job():
    print("Executing backup at {}".format(datetime.datetime.now().isoformat()))
    backup_result = subprocess.check_output([BACKUP_SCRIPT_PATH])
    print(backup_result)
    print("Backup finished at {}".format(datetime.datetime.now().isoformat()))


if __name__ == "__main__":
    print("Starting periodic MongoDB backup")

    try:
        interval_hours = int(os.environ.get(INTERVAL_NAME, INTERVAL_DEFAULT))
    except:
        interval_hours = INTERVAL_DEFAULT

    print("Executing backups every {} hours".format(interval_hours))

    schedule.every(interval_hours).minutes.do(backup_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
