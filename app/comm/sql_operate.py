#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
from logger import get_logger
from sql_exec import MySqlExec
import os
from sys import path
commpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "comm"))
path.append(commpath)
path.append("../config")
from config.config import *
import json


log = get_logger(log_dir=LOG_DIR)

def add_user_to_db(user_name):
    """
    向name2id表中写入用户名
    :param user_name: 用户名 string
    :return:
    """
    sqlExec = MySqlExec(logger=log, ip=MYSQL_HOST, user=MYSQL_USR, passwd=MYSQL_PWD, port=MYSQL_PORT,
                        database=MYSQL_DBNAME)
    sqlExec.connectDb()
    # 直接添加用户名 若存在不会重复添加
    sql = "insert into chenlai.name2id (usr_name) values ('{usr_name}')".format(usr_name=user_name)
    log.info(">>添加用户名sql:\n%s" % (str(sql)))
    ret, result = sqlExec.exec_sql(sql)
    log.info(">>添加用户名结果: %d" % ret)
    log.info(">>向表中添加用户信息:\n用户名为：%s\n添加结果为：%s\n 1表示添加成功 -1表示该用户已存在" % (str(user_name), str(ret)))
    sqlExec.closeDb()
    rtn = {"ret": 0, "result": ""}
    return rtn

def download_info_to_db(rsp, user_name):
    """
    将调用download接口的信息写入数据库
    :param rsp: {"ret": 1, "errno": 55000000, "excepInfo": "输入用户名不能为空", "detail": {}}
    :param user_name:
    :return:
    """
    sqlExec = MySqlExec(logger=log, ip=MYSQL_HOST, user=MYSQL_USR, passwd=MYSQL_PWD, port=MYSQL_PORT,
                        database=MYSQL_DBNAME)
    sqlExec.connectDb()

    sql = "select id from chenlai.name2id where usr_name='{user_name}'".format(user_name=user_name)
    log.info(">>查询name2id表sql:\n%s" % (str(sql)))
    ret, result = sqlExec.exec_sql(sql)
    log.info(">>查询name2id表结果: %d" % ret)
    # 数据库有问题给个返回 置标志位 把错误信息返回去
    if ret == -1:
        rtn = {"ret": ret, "result": result}
        return rtn
    # 获取name2id的id 外键 operation&download_detail的usr_id
    usr_id = str(json.loads(result)[0]["id"])
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 往operation表中写入数据
    sql = "insert into chenlai.operation (usr_id, oprn, oprntime) values ('{usr_id}', 'down', '{dt}')".format(
        usr_id=usr_id,
        dt=dt)
    log.info(">>写入operation表sql:\n%s" % (str(sql)))
    ret, result = sqlExec.exec_sql(sql)
    log.info(">>写入operation表结果: %d" % ret)
    if ret == -1:
        rtn = {"ret": ret, "result": result}
        return rtn
    # 往download_detail写入
    # 判断detail是否需要字符串截取
    detail = str(rsp['detail']).replace("'", '"')
    is_full_detail = 'Y'
    if len(detail) > 256:
        detail = detail[:256]
        is_full_detail = 'N'
    ret = rsp['ret']
    errno = rsp['errno']

    sql = "insert into chenlai.download_detail (usr_id, ret, errno, is_full_detail, detail) values ('{usr_id}', " \
          "'{ret}', '{errno}','{is_full_detail}', '{detail}')".format(usr_id=usr_id, ret=ret, errno=errno,
                                                                      is_full_detail=is_full_detail, detail=detail)
    log.info(">>写入download_detail表sql:\n%s" % (str(sql)))
    ret, result = sqlExec.exec_sql(sql)
    log.info(">>写入download_detail表结果: %d" % ret)
    if ret == -1:
        rtn = {"ret": ret, "result": result}
        return rtn
    sqlExec.closeDb()
    rtn = {"ret": 0, "result": ""}
    return rtn

def cmd_info_to_db(rsp, user_name):
    """
    将调用runCmd接口的信息写入数据库
    :param rsp:
    :return:
    """
    sqlExec = MySqlExec(logger=log, ip=MYSQL_HOST, user=MYSQL_USR, passwd=MYSQL_PWD, port=MYSQL_PORT,
                        database=MYSQL_DBNAME)
    sqlExec.connectDb()

    sql = "select id from chenlai.name2id where usr_name='{user_name}'".format(user_name=user_name)
    log.info(">>查询name2id表sql:\n%s" % (str(sql)))
    ret, result = sqlExec.exec_sql(sql)
    log.info(">>查询name2id表结果: %d" % ret)
    if ret == -1:
        rtn = {"ret": ret, "result": result}
        return rtn
    # 获取name2id的id
    usr_id = str(json.loads(result)[0]["id"])
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 往operation表中插入数据
    sql = "insert into chenlai.operation (usr_id, oprn, oprntime) values ('{usr_id}', 'cmd', '{dt}')".format(
        usr_id=usr_id,
        dt=dt)
    log.info(">>写入operation表sql:\n%s" % (str(sql)))
    ret, result = sqlExec.exec_sql(sql)
    log.info(">>写入operation表结果: %d" % ret)
    if ret == -1:
        rtn = {"ret": ret, "result": result}
        return rtn
    # 往shell_detail写入
    # 判断detail是否需要字符串截取
    detail = str(rsp['detail']).replace("'", '"')
    is_full_detail = 'Y'
    if len(detail) > 256:
        detail = detail[:256]
        is_full_detail = 'N'
    # 判断msg是否需要字符串截取
    is_full_msg = 'Y'
    ret_msg = str(rsp['return_msg']).replace("'", '"')
    if len(ret_msg) > 256:
        ret_msg = ret_msg[:256]
        is_full_msg = 'N'
    ret = rsp['ret']
    errno = rsp['errno']

    sql = "insert into chenlai.shell_detail (usr_id, ret, errno, is_full_msg, ret_msg, is_full_detail, detail) " \
          "values ('{usr_id}', '{ret}', '{errno}','{is_full_msg}', '{ret_msg}', '{is_full_detail}', '{detail}')".format(
        usr_id=usr_id, ret=ret, errno=errno, is_full_msg=is_full_msg, ret_msg=ret_msg,
        is_full_detail=is_full_detail, detail=detail)
    log.info(">>写入shell_detail表sql:\n%s" % (str(sql)))
    ret, result = sqlExec.exec_sql(sql)
    log.info(">>写入shell_detail表结果: %d" % ret)
    if ret == -1:
        rtn = {"ret": ret, "result": result}
        return rtn

    sqlExec.closeDb()

    rtn = {"ret": 0, "result": ""}
    return rtn

def query_info_to_db(rsp, user_name):
    """
    将调用history接口的信息写入数据库
    :param rsp:
    :return:
    """
    sqlExec = MySqlExec(logger=log, ip=MYSQL_HOST, user=MYSQL_USR, passwd=MYSQL_PWD, port=MYSQL_PORT,
                        database=MYSQL_DBNAME)
    sqlExec.connectDb()

    sql = "select id from chenlai.name2id where usr_name='{user_name}'".format(user_name=user_name)
    log.info(">>查询name2id表sql:\n%s" % (str(sql)))
    ret, result = sqlExec.exec_sql(sql)
    log.info(">>查询name2id表结果: %d" % ret)
    if ret == -1:
        rtn = {"ret": ret, "result": result}
        return rtn
    # 获取name2id的id
    usr_id = str(json.loads(result)[0]["id"])
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 往operation表中写入数据
    sql = "insert into chenlai.operation (usr_id, oprn, oprntime) values ('{usr_id}', 'qury', '{dt}')".format(
        usr_id=usr_id,
        dt=dt)
    log.info(">>写入operation表sql:\n%s" % (str(sql)))
    ret, result = sqlExec.exec_sql(sql)
    log.info(">>写入operation表结果: %d" % ret)
    if ret == -1:
        rtn = {"ret": ret, "result": result}
        return rtn
    # 往sql_detail写入
    # 判断detail是否需要字符串截取
    detail = str(rsp['detail']).replace("'", '"')
    is_full_detail = 'Y'
    if len(detail) > 256:
        detail = detail[:256]
        detail = eval(repr(detail).replace('\\', ''))
        is_full_detail = 'N'
    ret = rsp['ret']
    errno = rsp['errno']
    sql = "insert into chenlai.sql_detail (usr_id, ret, errno, is_full_detail, detail) values ('{usr_id}', '{ret}', " \
          "'{errno}','{is_full_detail}', '{detail}')".format(usr_id=usr_id, ret=ret, errno=errno,
                                                             is_full_detail=is_full_detail, detail=detail)
    log.info(">>写入sql_detail表sql:\n%s" % (str(sql)))
    ret, result = sqlExec.exec_sql(sql)
    log.info(">>写入sql_detail表结果: %d" % ret)
    if ret == -1:
        rtn = {"ret": ret, "result": result}
        return rtn

    sqlExec.closeDb()

    rtn = {"ret": 0, "result": ""}
    return rtn
