#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script that runs a MongoDB backup job periodically according 
to the interval defined by the INTERVAL_NAME environment variable.
"""

import time
import datetime
import subprocess
import functools
import traceback
import os
import sys

import schedule

BACKUP_SCRIPT_PATH = "/app/backup.sh"
INTERVAL_NAME = "BACKUP_INTERVAL"


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
        interval_hours = int(os.environ.get(INTERVAL_NAME))
    except:
        raise ValueError("Undefined or invalid interval variable: {}".format(INTERVAL_NAME))

    print("Executing backups every {} hours".format(interval_hours))

    schedule.every(interval_hours).hours.do(backup_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
