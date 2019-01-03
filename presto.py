import os
import re
from config.appconf import AppConf
from kvtable import KVTable

STORED_AS_PARQUET_STR = " STORED AS PARQUET;"
PARTITION_INTERVAL_RE = r"([0-9]+)([a-zA-Z]+)"


class Presto:

    def __init__(self, logger, view_name, partition_str, conf=AppConf, kvtable=KVTable()):
        self.logger = logger
        self.view_name = view_name
        self.partition_str = partition_str
        self.second_table_schema = conf.hive_schema
        self.second_table = kvtable.get_parquet_table_name()
        self.conf = conf
        self.kvtable = kvtable

    def generate_unified_view(self):
        attributes = self.convert_schema()
        str = "CREATE VIEW "+self.view_name+" as ( SELECT "+attributes
        str += " FROM "+self.kvtable.container_name+"."+self.kvtable.name
        str += " UNION ALL SELECT "+attributes
        str += " FROM "+self.second_table_schema+"."+self.second_table
        str += ")"
        return str

    def generate_partition_by(self):
        part = re.match(PARTITION_INTERVAL_RE, self.partition_str).group(2)
        if part == 'y':
            partition_by = ",year"
        if part == 'm':
            partition_by = ",year,month"
        if part == 'd':
            partition_by = ",year,month,day"
        if part == 'h':
            partition_by = ",year,month,day,hour"
        return partition_by

    def convert_schema(self):
        schema_fields = self.kvtable.get_schema_fields()
        schema_fields += self.generate_partition_by()
        return schema_fields

    def stored_by_parquet(self):
        str = " STORED AS PARQUET;"
        return str

    def execute_command(self):
        script = self.generate_unified_view()
        self.logger.debug(script)
        os.system("/opt/presto/bin/presto-cli.sh --server http://localhost:8889 --catalog hive --schema default --execute \"" + script + "\"")


