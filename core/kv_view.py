from datetime import datetime, timedelta
import re

KV_VIEW_FILE_NAME = "create_kv_view.txt"
PARTITION_INTERVAL_RE = r"([0-9]+)([a-zA-Z]+)"

# TODO: Add verification that hive table created (handle Trying to send on a closed client exception


class KVView(object):
    def __init__(self, logger, real_time_window, conf, kv_table):
        self.logger = logger
        self.kv_table = kv_table
        self.name = self.kv_table.name + "_view"
        self.real_time_window = real_time_window
        self.conf = conf

    def parse_real_time_window(self):
        now = datetime.now()
        part = re.match(PARTITION_INTERVAL_RE, self.real_time_window).group(2)
        val = int(re.match(PARTITION_INTERVAL_RE, self.real_time_window).group(1))
        self.logger.debug("generate time window".format(part))
        if part == 'd':
            window_time = now - timedelta(days=val)
        if part == 'h':
            window_time = now - timedelta(hours=val)
        return window_time

    def generate_where_clause(self):
        window_time = self.parse_real_time_window()
        part = re.match(PARTITION_INTERVAL_RE, self.real_time_window).group(2)
        self.logger.debug("generate_partition_by {0}".format(part))
        condition = ''
        if part == 'y':
            condition += "year="+str(window_time.year)
        if part == 'm':
            condition += "year="+str(window_time.year)+" AND month="+str(window_time.month)
        if part == 'd':
            condition += "year=" + str(window_time.year) + " AND month=" + str(window_time.month)+" AND day=" \
                         + str(window_time.day)
        if part == 'h':
            condition += "year=" + str(window_time.year) + " AND month=" + str(window_time.month) + " AND day=" + \
                        str(window_time.day) + " AND hour="+str(window_time.hour)
        clause = " WHERE "+condition
        return clause

    def create_view_prefix(self):
        hive_prefix = "hive." + self.conf.hive_schema + "."
        prefix = "CREATE OR REPLACE VIEW " + hive_prefix + self.kv_table.name + \
                 "_view AS SELECT * FROM " + hive_prefix + self.kv_table.name
        return prefix

    def create_view(self):
        import os
        hive_path = self.conf.hive_home
        command = hive_path + " -f " + KV_VIEW_FILE_NAME
        self.logger.info("Create Hive table command : " + command)
        os.system(command)

    def generate_crete_view_script(self):
        try:
            self.logger.debug("generating kv view script")
            prefix = self.create_view_prefix()
            clause = self.generate_where_clause()
            script = prefix + clause
            self.logger.debug("create kv view script {}".format(script))
            f = open(KV_VIEW_FILE_NAME, "w")
            f.write(script)
            f.close()
            self.create_view()
        except Exception as e:
            self.logger.error(e)
            raise





