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

import schedule

BACKUP_SCRIPT_PATH = "/app/backup.sh"
ENV_BACKUP_INTERVAL = "BACKUP_INTERVAL"
ENV_BACKUP_TIME = "BACKUP_TIME"
TIME_FORMAT = "%H:%M"


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
    print("Starting periodic MongoDB backup at {}".format(datetime.datetime.now().isoformat()))

    try:
        interval_days = int(os.environ.get(ENV_BACKUP_INTERVAL))
    except:
        raise ValueError("Undefined or invalid var: {}".format(ENV_BACKUP_INTERVAL))

    try:
        backup_time = os.environ.get(ENV_BACKUP_TIME)
        datetime.datetime.strptime(backup_time, TIME_FORMAT)
    except:
        raise ValueError("Undefined or invalid var: {}".format(ENV_BACKUP_TIME))

    print("Executing backups every {} day/s at {}".format(interval_days, backup_time))

    schedule.every(interval_days).days.at(backup_time).do(backup_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
