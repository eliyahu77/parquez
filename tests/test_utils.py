from utils.logger import Logger
from config.app_conf import AppConf
from utils.utils import Utils


# test_utils.py
def test_copy_v3io_file():
    logger = Logger()
    logger.info("logging......")
    conf = AppConf(logger, "test.ini")
    utils = Utils(logger, conf)
    utils.copy_to_v3io("../v3io-spark2-tools_2.11.jar")


def test_list_containers():
    logger = Logger()
    logger.info("logging......")
    conf = AppConf(logger, "test.ini")
    utils = Utils(logger, conf)
    utils.list_containers()




