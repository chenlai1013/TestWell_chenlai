import os

# 数据库配置信息
# MYSQL_HOST = "106.52.209.84"  这里现存问题是指明ip会time out  todo
MYSQL_HOST = "0.0.0.0"
MYSQL_PORT = "3306"
MYSQL_USR = "root"
MYSQL_PWD = "QWERop[]2016"
MYSQL_DBNAME = "chenlai"
SECRET_KEY = "QWERop[]2016"
RUNCMD_TIMEOUT = 5


LOG_DIR = "{}/log".format(
    os.getcwd()
)