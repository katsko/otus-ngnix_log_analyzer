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
    'REPORT_DIR': './reports',
    'LOG_DIR': './log',
    'LOG_NAME_PATTERN': r'^nginx-access-ui.log-\d{8}(\.gz|)$',
    'LOG_NAME_SLICE': slice(20, 28)
}


def search_last_log_file(config):
    log_dir = Path(config['LOG_DIR'])
    new_date_str = ''
    new_date = None
    new_file_path = None
    pattern = re.compile(config['LOG_NAME_PATTERN'])
    log_sl = config['LOG_NAME_SLICE']
    for file_name in os.listdir(log_dir):
        if (pattern.search(file_name) and
                os.path.isfile(log_dir / file_name) and
                new_date_str < file_name[log_sl]):
            try:
                new_date = datetime.strptime(
                    file_name[log_sl], '%Y%m%d').date()
                new_date_str = file_name[log_sl]
                new_file_path = log_dir / file_name
            except ValueError:
                pass
    return new_date, new_file_path


def main():
    print(search_last_log_file(config))


if __name__ == "__main__":
    main()
