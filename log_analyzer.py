#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime
from pathlib import Path


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip '
#                     '[$time_local] "$request" $status $body_bytes_sent '
#                     '"$http_referer" "$http_user_agent" '
#                     '"$http_x_forwarded_for" "$http_X_REQUEST_ID" '
#                     '"$http_X_RB_USER" $request_time';

config = {
    'REPORT_SIZE': 1000,
    'LOG_DIR': './log',
    'LOG_NAME_PATTERN': r'^nginx-access-ui.log-\d{8}(\.gz|)$',
    'LOG_DATE_FORMAT': '%Y%m%d',
    'LOG_NAME_SLICE': slice(20, 28),
    'REPORT_DIR': './reports',
    'REPORT_NAME_PATTERN': r'^report-\d{4}.\d{2}.\d{2}.html$',
    'REPORT_DATE_FORMAT': '%Y.%m.%d',
    'REPORT_NAME_SLICE': slice(7, 17),
}


def search_last_file(directory, pattern, date_format, sl, new_date_str=''):
    new_date = None
    new_file_path = None
    for file_name in os.listdir(directory):
        if (pattern.search(file_name) and
                os.path.isfile(directory / file_name) and
                new_date_str < file_name[sl]):
            try:
                new_date = datetime.strptime(
                    file_name[sl], date_format).date()
                new_date_str = file_name[sl]
                new_file_path = directory / file_name
            except ValueError:
                pass
    return new_date, new_file_path


def main():
    report_dir = Path(config['REPORT_DIR'])
    pattern = re.compile(config['REPORT_NAME_PATTERN'])
    date_format = config['REPORT_DATE_FORMAT']
    report_sl = config['REPORT_NAME_SLICE']
    result = search_last_file(report_dir, pattern, date_format, report_sl)
    print(result)

    log_dir = Path(config['LOG_DIR'])
    pattern = re.compile(config['LOG_NAME_PATTERN'])
    date_format = config['LOG_DATE_FORMAT']
    log_sl = config['LOG_NAME_SLICE']
    result = search_last_file(log_dir, pattern, date_format, log_sl)
    print(result)


if __name__ == "__main__":
    main()
