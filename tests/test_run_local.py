from conftest import (
    examples_path, has_secrets, here, out_path, tag_test, verify_state
)
from mlrun import NewTask, run_local, code_to_function
from mlrun import NewTask, get_run_db, new_function

ARTIFACTS_PATH = ''

base_spec = NewTask(params={'view_name': 'view_name'
    , 'partition_by': 'h'
    , 'partition_interval': '1h'
    , 'real_time_window': '1d'
    , 'historical_retention': '7d'
    , 'real_time_table_name': 'faker'
    , 'config_path': 'test.ini'}, out_path=out_path)


def test_run_local_get_schema():
    spec = tag_test(base_spec, 'test_run_local_parquet')
    result = run_local(spec, command='../get_table_schema.py', workdir='./', artifact_path='./artifacts')
    verify_state(result)


def test_run_local_parquet():
    spec = tag_test(base_spec, 'test_run_local_parquet')
    result = run_local(spec, command='../create_parquet_table.py', workdir='./', artifact_path='./artifacts')
    verify_state(result)


def test_run_create_kv_view():
    spec = tag_test(base_spec, 'test_run_create_kv_view')
    result = run_local(spec, command='../create_kv_view.py', workdir='./', artifact_path='./artifacts')
    verify_state(result)