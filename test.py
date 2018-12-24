#!/usr/bin/env python3

import datetime
import unittest
from unittest import mock
from pathlib import Path

import log_analyzer


class TestSuite(unittest.TestCase):

    def test_search_last_log_file(self):
        def isfile_side_effect(file_path):
            log_dir = Path(log_analyzer.config['LOG_DIR'])
            path_map = {
                log_dir / 'nginx-access-ui.log-20170630.gz': True,
                log_dir / 'dir1': False,
                log_dir / 'nginx-access-ui.log-20180630': True,
                log_dir / 'nginx-access-ui.log-20180632': True,
                log_dir / 'nginx-access-ui.log-201AAA30.gz': True,
                log_dir / 'pic.jpg': True}
            return path_map[file_path]

        with mock.patch('os.listdir') as mocked_listdir:
            with mock.patch('os.path.isfile') as mocked_isfile:
                mocked_listdir.return_value = [
                    'nginx-access-ui.log-20170630.gz',
                    'dir1',
                    'nginx-access-ui.log-20180630',
                    'nginx-access-ui.log-20180632',
                    'nginx-access-ui.log-201AAA30.gz',
                    'pic.jpg']
                mocked_isfile.side_effect = isfile_side_effect
                result = log_analyzer.search_last_log_file(log_analyzer.config)
        log_dir = Path(log_analyzer.config['LOG_DIR'])
        new_date = datetime.date(2018, 6, 30)
        new_file_name = 'nginx-access-ui.log-20180630'
        new_file_path = log_dir / new_file_name
        self.assertEqual(result, (new_date, new_file_path))


if __name__ == "__main__":
    unittest.main()
