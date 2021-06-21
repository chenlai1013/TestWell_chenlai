#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
flask框架代码各部分介绍：
1. 导入Flask扩展
2. 创建Flask应用程序实例
3. 定义路由及视图函数  Flask中定义路由是通过装饰器实现的
4. 启动程序
"""

import json
import traceback
import urllib.request
import requests
import subprocess
import tempfile
from pathlib import Path
from flask import Flask
from flask import request
from flask import jsonify
from config.config import *
from comm import logger
from comm.sql_exec import MySqlExec
from comm.sql_operate import add_user_to_db, download_info_to_db, cmd_info_to_db, query_info_to_db


log = logger.get_logger(log_dir=LOG_DIR)

app = Flask(__name__)  # __name__是为了确定资源所在路径


@app.route('/api/download', methods=["POST"])
def download():
    """
    下载文件到指定本地目录
    下载文件应该支持单一路径和批量路径，本地目录 1：可为空 默认当前同级目录 2. 绝对目录 3. 相对目录
    request:
    {
        "user_name": ""
        "url_list":["http://download.redis.io/releases/redis-5.0.5.tar.gz",
        "https://pythondict.com/wp-content/uploads/2019/07/2019073115192114.jpg"],
        "local_path":""
    }
    'user_name': 用户名
    'url_list': 待下载文件的列表
    'local_path': 存储目录路径
    :return: 成功或者失败的响应 若失败报出对应的错
    {
    "detail": {
        "success files": ["http://download.redis.io/releases/redis-5.0.5.tar.gz",
            "https://pythondict.com/wp-content/uploads/2019/07/2019073115192114.jpg"
        ]
    },
    "errno": "",
    "excepInfo": "操作执行成功",
    "ret": 0
}
    """
    bytesPara = request.get_data()

    dictPara = json.loads(str(bytesPara, encoding="utf8"))
    log.info(">>dictPara:\n%s" % (str(dictPara)))

    # 定义返回数据包字段及含义  标志位ret为0表示成功 为1表示失败
    rsp = {"ret": 1, "errno": 50000000, "excepInfo": "文件异常或指定目录异常", "detail": {}}
    try:
        # 首先判断用户名 若为空 直接返回
        if not dictPara['user_name']:
            rsp = {"ret": 1, "errno": 54000001, "excepInfo": "输入用户名不能为空", "detail": {}}
            log.error("输入用户名为空")
            return jsonify(rsp)
        # 数据库中写入用户名
        add_user_to_db(dictPara['user_name'])

        # 执行操作
        # 默认存储在当前路径
        if not dictPara['local_path']:
            dictPara['local_path'] = os.getcwd()
        else:
            # 判断路径是否合法
            locals_path = Path(dictPara['local_path'])
            if not locals_path.exists() or not locals_path.is_dir():
                rsp = {"ret": 1, "errno":"50001001", "excepInfo": "指定目录不存在或非文件夹目录", "detail": {}}
                log.error("指定目录不存在或非文件夹目录:\n%s" % str(dictPara['local_path']))
                # 写入数据库
                sql_rtn = download_info_to_db(rsp, dictPara['user_name'])
                if sql_rtn["ret"] == -1:
                    rsp = {"ret": 1, "errno": 53001001, "excepInfo": "数据库写入download出错", "detail": sql_rtn["result"]}
                    log.error("数据库写入download出错")
                return jsonify(rsp)

        for url in dictPara['url_list']:
            # 验证单个url是否可以访问 若单个有问题，记录到detail中
            with requests.head(url) as file:
                if file.status_code != 200:
                    if "error files" not in rsp['detail']:
                        rsp['detail']["error files"] = [url]
                    else:
                        rsp['detail']["error files"].append(url)
                else:
                    if "success files" not in rsp['detail']:
                        rsp['detail']["success files"] = [url]
                    else:
                        rsp['detail']["success files"].append(url)
                    file_path = os.path.join(dictPara['local_path'], 'download_file')
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    down_path = os.path.join(file_path, url.split('/')[-1])
                    urllib.request.urlretrieve(url, filename=down_path)

        # 封装rsp
        # 部分文件下载失败
        if "error files" in rsp['detail'] and "success files" in rsp['detail']:
            rsp = {"ret": 0, "errno": "50002001", "excepInfo": "部分url文件不存在", "detail": rsp['detail']}
            log.error("部分url文件不存在:\n%s" % str(rsp))
        elif "error files" in rsp['detail']:
            rsp = {"ret": 1, "errno": "50002002", "excepInfo": "全部url文件不存在", "detail": rsp['detail']}
            log.error("全部url文件不存在:\n%s" % str(rsp))
        elif "success files" in rsp['detail']:
            rsp = {"ret": 0, "errno": "", "excepInfo": "操作执行成功", "detail": rsp['detail']}
            log.info("所有文件下载成功:\n%s" % str(rsp))
        else:
            rsp = {"ret": 1, "errno": "50002003", "excepInfo": "输入url为空", "detail": {}}
            log.info("输入url为空")

        # 写入数据库
        sql_rtn = download_info_to_db(rsp, dictPara['user_name'])
        if sql_rtn["ret"] == -1:
            rsp = {"ret": 1, "errno": 53001001, "excepInfo": "数据库写入download出错", "detail": sql_rtn["result"]}
            log.error("数据库写入download出错")


    except Exception as e:
        info = traceback.format_exc()
        rsp["excepInfo"] = str(info)
        rsp["errno"] = "50000001"
        log.error("执行下载文件，抛异常:\n%s" % str(info))
        # 写入数据库
        sql_rtn = download_info_to_db(rsp, dictPara['user_name'])
        if sql_rtn["ret"] == -1:
            rsp = {"ret": 1, "errno": 53001001, "excepInfo": "数据库写入download出错", "detail": sql_rtn["result"]}
            log.error("数据库写入download出错")

    rsp = jsonify(rsp)
    return rsp


@app.route('/api/runCmd', methods=["POST"])
def runCmd():
    """
    本地执行shell命令/shell脚本  cmd 执行命令
    request:
    {
        "user_name": ""
        "cmd":"",
        "timeout":"",
    }
    :return: 成功或者失败的响应 若失败报出对应的错 执行命令后有返回的应该给出

    """

    bytesPara = request.get_data()
    dictPara = json.loads(str(bytesPara, encoding="utf8"))
    log.info(">>dictPara:\n%s" % (str(dictPara)))

    if not dictPara["timeout"]:
        dictPara["timeout"] = RUNCMD_TIMEOUT
    # 所有分支都是直接完全填充rsp 故这里未被使用 只是做个格式说明
    rsp = {"ret": 1, "errno": 51000000, "excepInfo": "cmd执行出错", "return_msg": "", "detail": {}}
    try:
        # 用户名为空 直接返回
        if not dictPara['user_name']:
            rsp = {"ret": 1, "errno": 54000001, "excepInfo": "输入用户名不能为空"}
            log.error("输入用户名为空")
            return rsp
        # 数据库中写入用户名
        add_user_to_db(dictPara['user_name'])

        # 为避免子进程往父进程写时管道阻塞，使用临时文件存子进程输出
        # 得到一个临时文件对象， 调用close后，此文件从磁盘删除
        temp_opt = tempfile.TemporaryFile(mode='w+')
        # 获取临时文件的文件号
        fileno = temp_opt.fileno()

        # 执行shell 输出结果存入临时文件
        sps = subprocess.Popen(dictPara["cmd"], shell=True, stdout=fileno, stderr=fileno, encoding="utf-8")
        sps.wait(timeout=int(dictPara["timeout"]))
        # 从临时文件读出shell命令的输出结果
        temp_opt.seek(0)
        ret_file = temp_opt.read()
        # 以换行符拆分数据，并去掉换行符号存入列表
        ret_list = ret_file.strip().split('\n')

        if sps.returncode == 0:
            rsp = {"ret": 0, "errno":"", "excepInfo": "cmd执行成功", "return_msg": ret_list, "detail": {}}
            log.info("cmd执行成功>>:\n%s" % (str(rsp)))
        else:
            rsp = {"ret": 1, "errno": 51001001, "excepInfo": "cmd执行失败", "return_msg": "", "detail": ret_list}
            log.error("cmd执行失败>>:\n%s" % (str(rsp)))

        # 写入数据库
        sql_rtn = cmd_info_to_db(rsp, dictPara['user_name'])
        if sql_rtn["ret"] == -1:
            rsp = {"ret": 1, "errno": 53002001, "excepInfo": "数据库写入cmd出错", "detail": sql_rtn["result"]}
            log.error("数据库写入cmd出错")

    except Exception as e:
        info = traceback.format_exc()
        rsp = {"ret": 1, "errno": 51000001, "excepInfo": "cmd执行出现异常导致失败", "return_msg": "", "detail": info}
        log.error("cmd执行失败，抛异常:\n%s" % str(info))
        # 写入数据库
        sql_rtn = cmd_info_to_db(rsp, dictPara['user_name'])
        if sql_rtn["ret"] == -1:
            rsp = {"ret": 1, "errno": 53002001, "excepInfo": "数据库写入cmd出错", "detail": sql_rtn["result"]}
            log.error("数据库写入cmd出错")
        if temp_opt:
            temp_opt.close()
    rsp = jsonify(rsp)
    return rsp

@app.route('/api/history', methods=["POST"])
def history():
    """
    操作记录查询并返回分页数据 或按条件查询的结果
    输入需要考虑条件查询
    limit有个默认值 也可以输入
    request:
    {
        "user_name": ""
        "sql_demand":{
            "operator": "",
            "operation": ["download", "shell", "sql"] ,
            "oprntime": {"start_time": "", "end_time":""},  # 输入格式  "1900-01-01 00:00:00"
            "ret": "",
            "limit": 10,
            "offset": 0
        }
    }
    :return: 成功或者失败的响应 若失败报出对应的错 成功返回的是表！！
    """
    bytesPara = request.get_data()
    dictPara = json.loads(str(bytesPara, encoding="utf8"))
    log.info(">>dictPara:\n%s" % (str(dictPara)))

    # 定义返回数据包字段及含义  标志位ret为0表示成功 为1表示失败
    rsp = {"ret": 1, "errno": 52000000, "excepInfo": "查询数据库失败", "detail": {"download":"", "shell":"", "sql":""}}
    try:
        # 用户名为空 直接返回
        if not dictPara['user_name']:
            rsp = {"ret": 1, "errno": 54000001, "excepInfo": "输入用户名不能为空"}
            log.error("输入用户名为空")
            return jsonify(rsp)
        # 数据库中写入用户名
        add_user_to_db(dictPara['user_name'])

        # 执行操作 查询db
        sqlExec = MySqlExec(logger=log, ip=MYSQL_HOST, user=MYSQL_USR, passwd=MYSQL_PWD, port=MYSQL_PORT,
                            database=MYSQL_DBNAME)
        sqlExec.connectDb()
        # 条件查询组装
        start_time = dictPara['sql_demand']["oprntime"]["start_time"]
        end_time = dictPara['sql_demand']["oprntime"]["end_time"]
        lmt = dictPara['sql_demand']["limit"]
        oft = dictPara['sql_demand']["offset"]
        qry_demand = {"operator": "1=1", "ret": "1=1", "qry_time": "1=1", "limit": 10, "offset": 0}
        if not start_time:
            start_time = '1900-01-01 00:00:00'
        if not end_time:
            end_time = '2200-12-31 23:59:59'
        if lmt:
            qry_demand["limit"] = int(lmt)
        if oft:
            qry_demand["offset"] = int(oft)
        qry_demand["qry_time"] = "operation.oprntime between '{start_time}' and '{end_time}'".format(
            start_time=start_time, end_time=end_time)
        if dictPara["sql_demand"]["operator"]:
            qry_demand["operator"] = "name2id.usr_name=" + "'" + str(dictPara["sql_demand"]["operator"]) + "'"
        # 按条件查询
        # 首先判断操作 默认全查
        if not dictPara["sql_demand"]["operation"]:
            dictPara["sql_demand"]["operation"] = ["download", "shell", "sql"]
        # 方案1：全连接三张表得到所有数据再根据要求过滤操作
        # 方案2：通过选择分支 去简单过滤操作
        # 选择方案2
        for otn in dictPara["sql_demand"]["operation"]:
            if otn == "download":
                if dictPara["sql_demand"]["ret"] == "1" or dictPara["sql_demand"]["ret"] == "0":
                    qry_demand["ret"] = "download_detail.ret=" + "'" + str(dictPara["sql_demand"]["ret"]) + "'"
                sql = "select name2id.usr_name, operation.oprn, operation.oprntime, download_detail.ret, " \
                      "download_detail.errno, download_detail.is_full_detail, download_detail.detail " \
                      "from name2id left join operation on name2id.id=operation.usr_id left join download_detail on " \
                      "name2id.id=download_detail.usr_id where {operator} and {ret} and {qry_time} limit {limit}" \
                      " offset {offset}".format(**qry_demand)
            elif otn == "shell":
                if dictPara["sql_demand"]["ret"]:
                    qry_demand["ret"] = "shell_detail.ret=" + "'" + str(dictPara["sql_demand"]["ret"]) + "'"
                sql = "select name2id.usr_name, operation.oprn, operation.oprntime, shell_detail.ret, " \
                      "shell_detail.errno, shell_detail.is_full_msg, shell_detail.ret_msg, shell_detail.is_full_detail, " \
                      "shell_detail.detail from name2id left join operation on name2id.id=operation.usr_id left join shell_detail on " \
                      "name2id.id=shell_detail.usr_id where {operator} and {ret} and {qry_time} limit {limit}" \
                      " offset {offset}".format(**qry_demand)
            elif otn == "sql":
                if dictPara["sql_demand"]["ret"]:
                    qry_demand["ret"] = "sql_detail.ret=" + "'" + str(dictPara["sql_demand"]["ret"]) + "'"
                sql = "select name2id.usr_name, operation.oprn, operation.oprntime, sql_detail.ret, " \
                      "sql_detail.errno, sql_detail.is_full_detail, sql_detail.detail " \
                      "from name2id left join operation on name2id.id=operation.usr_id left join sql_detail on " \
                      "name2id.id=sql_detail.usr_id where {operator} and {ret} and {qry_time} limit {limit}" \
                      " offset {offset}".format(**qry_demand)
            else:
                pass
            ret, result = sqlExec.exec_sql(sql)
            if ret == -1:
                rsp = {"ret": 1, "errno": 52001001, "excepInfo": "数据库查询数据出错", "detail":result}
                log.error("数据库查询数据出错")
                sql_rtn = query_info_to_db(rsp, dictPara['user_name'])
                if sql_rtn["ret"] == -1:
                    rsp = {"ret": 1, "errno": 53003001, "excepInfo": "数据库写入查询数据出错", "detail": sql_rtn["result"]}
                    log.error("数据库写入查询数据出错")
                return jsonify(rsp)
            rsp["detail"][otn] = result

        # 将此次操作写入数据库
        rsp["ret"] = 0
        rsp["errno"] = ""
        rsp["excepInfo"] = "写入数据库成功"
        sql_rtn = query_info_to_db(rsp, dictPara['user_name'])
        if sql_rtn["ret"] == -1:
            rsp = {"ret": 1, "errno": 53003001, "excepInfo": "数据库写入查询数据出错", "detail": sql_rtn["result"]}
            log.error("数据库写入查询数据出错")

    except Exception as e:
        info = traceback.format_exc()
        rsp["excepInfo"] = str(info)
        log.error("执行查询，抛异常:\n%s" % str(info))
        sql_rtn = query_info_to_db(rsp, dictPara['user_name'])
        if sql_rtn["ret"] == -1:
            rsp = {"ret": 1, "errno": 52000001, "excepInfo": "数据库写入查询数据异常报错", "detail": sql_rtn["result"]}
            log.error("数据库写入查询数据异常报错")

    rsp["ret"] = 0
    rsp["errno"] = ""
    rsp["excepInfo"] = "查询数据库成功"
    if rsp["detail"]["download"] == '[]' and rsp["detail"]["shell"] == '[]' and rsp["detail"]["sql"] == '[]':
        rsp["excepInfo"] = "查询数据库成功，但满足条件数据条数为0"
    rsp = jsonify(rsp)
    return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='12347', debug=True)
