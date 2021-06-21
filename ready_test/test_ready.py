#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from app.comm.sql_exec import MySqlExec
from app.comm import logger
from app.config.config import *
from ready_test.config_params import *
import requests
import json

log = logger.get_logger(log_dir=LOG_DIR)

class Test_Ready:
    def setup_class(self):
        # 整个类执行开始后
        # 连接数据库
        self.sqlExec = MySqlExec(logger=log, ip=MYSQL_HOST, user=MYSQL_USR, passwd=MYSQL_PWD, port=MYSQL_PORT,
                            database=MYSQL_DBNAME)
        self.sqlExec.connectDb()

    def teardown_class(self):
        # 整个类结束执行前
        # 关闭数据库
        self.sqlExec.closeDb()

    def test_download(self):
        """
        步骤:
        1. 确认db中无此id的数据
        2. 发送request 获得响应 判断 响应码是否为200 结果是否满足预期
        3. 再次确认数据库该id相应数据是否已经写入
        4. 删除数据库中相应数据
        :return:
        """
        url = test_download_param["url"]
        for i in range(len(test_download_param["downd_param"])):
            downd_param = test_download_param["downd_param"][i]
            print("test case为:", downd_param["case_name"])
            params = {
                "user_name": test_download_param["user_name"],
                "url_list": downd_param["url_list"],
                "local_path": downd_param["local_path"],
            }

            # db确认是否存在
            sql = "select name2id.usr_name, name2id.id, download_detail.ret from chenlai.name2id left join chenlai.download_detail " \
                  "on name2id.id=download_detail.usr_id where name2id.usr_name='{usr_name}'".format(
                usr_name=params["user_name"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == downd_param["db_bf_ret"]

            # 发送request
            headers = {"content-type": "application/json"}
            ret = requests.post(url, data=json.dumps(params), headers=headers)
            assert ret.status_code == downd_param["request_code"]
            ret = json.loads(ret.text)
            assert ret["ret"] == downd_param["request_ret"]

            # db确认是否已经写入正确信息
            sql = "select name2id.usr_name, name2id.id, download_detail.ret from chenlai.name2id left join chenlai.download_detail " \
                  "on name2id.id=download_detail.usr_id where name2id.usr_name='{usr_name}'".format(usr_name=params["user_name"])
            ret, result_cfm = self.sqlExec.exec_sql(sql)

            assert ret == downd_param["db_write_ret"]
            result_cfm = json.loads(result_cfm[1:-1])
            assert result_cfm["ret"] == downd_param["db_cfm_ret"]

            # 删除db写入的信息
            sql = "delete from chenlai.download_detail where usr_id='{usr_id}'".format(usr_id=result_cfm["id"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == downd_param["db_del_dd_ret"]
            assert result == downd_param["db_del_dd_result"]

            sql = "delete from chenlai.operation where usr_id='{usr_id}'".format(usr_id=result_cfm["id"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == downd_param["db_del_opn_ret"]
            assert result == downd_param["db_del_opn_result"]
            sql = "delete from chenlai.name2id where id='{id}'".format(id=result_cfm["id"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == downd_param["db_del_n2i_ret"]
            assert result == downd_param["db_del_n2i_result"]

    def test_runcmd(self):
        """
        步骤:
        1. 确认db中无此id的数据
        2. 发送request 获得响应 判断 响应码是否为200 结果是否满足预期
        3. 再次确认数据库该id相应数据是否已经写入
        4. 删除数据库中相应数据
        :return:
        """
        url = test_runcmd_param["url"]
        for i in range(len(test_runcmd_param["runcmd_param"])):
            runcmd_param = test_runcmd_param["runcmd_param"][i]
            print("test case为:", runcmd_param["case_name"])
            params = {
                "user_name": test_runcmd_param["user_name"],
                "cmd": runcmd_param["cmd"],
                "timeout": runcmd_param["timeout"],
            }

            # db确认是否存在
            sql = "select name2id.usr_name, name2id.id, shell_detail.ret from chenlai.name2id left join " \
                  "chenlai.shell_detail on name2id.id=shell_detail.usr_id where name2id.usr_name='{usr_name}'".format(
                usr_name=params["user_name"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == runcmd_param["db_bf_ret"]

            # 发送request
            headers = {"content-type": "application/json"}
            ret = requests.post(url, data=json.dumps(params), headers=headers)
            assert ret.status_code == runcmd_param["request_code"]
            ret = json.loads(ret.text)
            assert ret["ret"] == runcmd_param["request_ret"]
            if runcmd_param["return_msg"] == 0:
                assert ret["return_msg"] == [''] or ret["return_msg"] == ''
            elif runcmd_param["return_msg"] == 1:
                assert ret["return_msg"] != None

            # db确认是否已经写入正确信息
            sql = "select name2id.usr_name, name2id.id, shell_detail.ret from chenlai.name2id left join chenlai.shell_detail " \
                  "on name2id.id=shell_detail.usr_id where name2id.usr_name='{usr_name}'".format(usr_name=params["user_name"])
            ret, result_cfm = self.sqlExec.exec_sql(sql)
            assert ret == runcmd_param["db_write_ret"]
            result_cfm = json.loads(result_cfm[1:-1])
            assert result_cfm["ret"] == runcmd_param["db_cfm_ret"]

            # 删除db写入的信息
            sql = "delete from chenlai.shell_detail where usr_id='{usr_id}'".format(usr_id=result_cfm["id"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == runcmd_param["db_del_dd_ret"]
            assert result == runcmd_param["db_del_dd_result"]

            sql = "delete from chenlai.operation where usr_id='{usr_id}'".format(usr_id=result_cfm["id"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == runcmd_param["db_del_opn_ret"]
            assert result == runcmd_param["db_del_opn_result"]
            sql = "delete from chenlai.name2id where id='{id}'".format(id=result_cfm["id"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == runcmd_param["db_del_n2i_ret"]
            assert result == runcmd_param["db_del_n2i_result"]


    def test_history(self):
        """
        步骤:
        1. 确认db中无此id的数据
        2. 发送request 获得响应 判断 响应码是否为200 结果是否满足预期
        3. 再次确认数据库该id相应数据是否已经写入
        4. 删除数据库中相应数据
        :return:
        """
        url = test_history_param["url"]
        for i in range(len(test_history_param["history_param"])):
            history_param = test_history_param["history_param"][i]
            print("test case为:", history_param["case_name"])
            params = {
                "user_name": test_history_param["user_name"],
                "sql_demand": {
                    "operator": history_param["operator"],
                    "operation": history_param["operation"],
                    "oprntime": {
                        "start_time": history_param["oprntime"]["start_time"],
                        "end_time": history_param["oprntime"]["end_time"],
                    },
                    "ret": history_param["ret"],
                    "limit": history_param["limit"],
                    "offset": history_param["offset"],
                }
            }

            # db确认是否存在
            sql = "select name2id.usr_name, name2id.id, shell_detail.ret from chenlai.name2id left join " \
                  "chenlai.shell_detail on name2id.id=shell_detail.usr_id where name2id.usr_name='{usr_name}'".format(
                usr_name=params["user_name"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == history_param["db_bf_ret"]

            # 发送request
            headers = {"content-type": "application/json"}
            ret = requests.post(url, data=json.dumps(params), headers=headers)
            assert ret.status_code == history_param["request_code"]
            ret = json.loads(ret.text)
            assert ret["ret"] == history_param["request_ret"]

            # db确认是否已经写入正确信息
            sql = "select name2id.usr_name, name2id.id, sql_detail.ret from chenlai.name2id left join chenlai.sql_detail " \
                  "on name2id.id=sql_detail.usr_id where name2id.usr_name='{usr_name}'".format(usr_name=params["user_name"])
            ret, result_cfm = self.sqlExec.exec_sql(sql)
            assert ret == history_param["db_write_ret"]
            result_cfm = json.loads(result_cfm[1:-1])
            assert result_cfm["ret"] == history_param["db_cfm_ret"]

            # 删除db写入的信息
            sql = "delete from chenlai.sql_detail where usr_id='{usr_id}'".format(usr_id=result_cfm["id"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == history_param["db_del_dd_ret"]
            assert result == history_param["db_del_dd_result"]

            sql = "delete from chenlai.operation where usr_id='{usr_id}'".format(usr_id=result_cfm["id"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == history_param["db_del_opn_ret"]
            assert result == history_param["db_del_opn_result"]
            sql = "delete from chenlai.name2id where id='{id}'".format(id=result_cfm["id"])
            ret, result = self.sqlExec.exec_sql(sql)
            assert ret == history_param["db_del_n2i_ret"]
            assert result == history_param["db_del_n2i_result"]

if __name__ == '__main__':
    pytest.main("-s -n test_ready.py")