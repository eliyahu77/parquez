import os
import re

PARTITION_BY_RE = r"([0-9]+)([a-zA-Z]+)"


class CronGenerator:

    def __init__(self, logger, conf, kv_table_name, partition_interval, key_value_window, historical_retention, partition_by):
        self.logger = logger
        self.conf =conf
        self.kv_table_name = kv_table_name
        self.partition_interval = partition_interval
        self.key_value_window = key_value_window
        self.historical_retention = historical_retention
        self.partition_by = partition_by

    def window_parser(self, window_type):
        m = re.match(PARTITION_BY_RE, window_type)
        result = ""
        if m.group(2) == 'm':
            result = m.group(1) + " minutes"
        if m.group(2) == 'h':
            result = m.group(1) + " hours"
        if m.group(2) == 'd':
            result = m.group(1) + " days"
        if m.group(2) == 'M':
            result = m.group(1) + " months"
        return result

    def partition_interval_parser(self):
        m = re.match(PARTITION_BY_RE, self.partition_interval)
        if m.group(2) == 'm':
            result = "*/" + m.group(1) + " * * * * "
        if m.group(2) == 'h':
            result = "0 " + "*/" + m.group(1) + " * * * "
        if m.group(2) == 'd':
            result = "0 * " + "*/" + m.group(1) + " * * "
        if m.group(2) == 'M':
            result = "0 * *" + "*/" + m.group(1) + " * "
        if m.group(2) == 'DW':
            result = "0 * * * " + "*/" + m.group(1)
        return result

    def create_cron_job(self):
        args6 = "'"+self.conf.hive_schema+"'"
        args5 = "'"+self.conf.v3io_container+"'"
        args4 = "'"+re.match(PARTITION_BY_RE, self.partition_by).group(2)+"'"
        args3 = "'"+self.window_parser(self.historical_retention)+"'"
        arg2 = "'"+self.window_parser(self.key_value_window)+"'"
        dirname, filename = os.path.split(os.path.abspath(__file__))

        command = "\"" + self.partition_interval_parser()+dirname+"/./parquetinizer.sh " + self.kv_table_name + " " +\
                  arg2 + " " + args3 + " " + args4 + " " + args5+" " + args6+"\""
        self.logger.debug(command)
        os.system(dirname+"/./parquetCronJob.sh " + command)
