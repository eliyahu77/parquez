from mlrun import get_or_create_ctx
from config.app_conf import AppConf
from core.parquet_table import ParquetTable
from utils.utils import Utils
from core.k8s_client import K8SClient
from core.params import Params

CONFIG_PATH = 'test.ini'


def get_bytes_from_file(filename):
    with open(filename, "r") as f:
        output = f.read()
    return output


def main(context):
    context.logger.info("loading configuration")
    conf = AppConf(context.logger, CONFIG_PATH)

    utils = Utils(context.logger, conf)
    params = Params()
    params.set_params_from_context(context)
    context.logger.info("generating parquet table")
    # load schema from artifacts
    #schema = context.get_input('schema')
    schema = get_bytes_from_file(context.artifact_path+"/parquet_schema.txt")

    parquet = ParquetTable(context.logger, conf, utils, params, schema, K8SClient(context.logger))
    parquet.generate_script()


if __name__ == '__main__':
    context = get_or_create_ctx('create-parquet-table')
    main(context)