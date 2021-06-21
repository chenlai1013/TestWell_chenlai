#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

import json
import re
import traceback
from collections import OrderedDict
from decimal import Decimal


import pymysql


class MySqlExec(object):
    def __init__(self, logger, ip="", user="", passwd="", port="",database=""):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.port = port
        self.database = database
        self.cur = None
        self.logger = logger

    def connectDb(self, dictPara=None):
        if dictPara is None:
            dictPara = {}
        if dictPara:
            self.ip = dictPara["ip"]
            self.user = dictPara["user"]
            self.passwd = dictPara["passwd"]
            self.port = dictPara["port"]
        #
        self.logger.info(
            "connect db:%s,%s,%s,%s,%s" % (self.ip, self.port, self.user, self.passwd, self.database)
        )
        if self.cur is None:
            self.conn = pymysql.connect(
                host=self.ip,
                port=int(self.port),
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                charset="utf8",
            )  # latin1
            # conn.autocommit(True)
            # self.conn.commit()
            self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
            # self.cur = self.conn.cursor()

    def closeDb(self):
        if self.cur != None:
            self.cur.close()
            self.cur = None
        #
        if self.conn != None:
            try:
                self.conn.close()
                self.conn = None
            except Exception as e:
                self.logger.info("close db con except:%s" % str(e))
        #
        self.logger.info("close db.\n")

    def sqlAppendLimit(self, sql, limit=10):
        if sql.find("select ") >= 0:
            if -1 == sql.find(" limit "):
                sql = sql.strip()
                if sql.endswith(";"):
                    sql = sql[:-1]
                #
                sql = sql + " limit %d ;" % limit
                self.logger.info("sql auto append limit %d" % limit)
        #
        return sql

    #
    # def switchDateTime(self,tupleV):
    #     lTupleV = len(tupleV)
    #     for i in range(0, lTupleV):
    #         for k1, v1 in tupleV[i].items():
    #             if type(v1) == datetime.datetime:
    #                 tupleV[i][k1] = v1.strftime("%Y-%m-%d %H:%M:%S")
    #
    # 调用这个接口
    def exec_sql(self, sql):
        result = ""
        self.logger.info("rcv sql:\n%s" % (sql))
        sqlList = sql.split("\n")
        sql = ""
        for s in sqlList:
            s = s.strip()
            if (not s.startswith("#")) and (s != ""):
                sql = sql + " " + s
        #
        # 中间有;号的语句，要分开发送mysql_store_result()。"Commands out of sync; you can't run this command now"
        # 处理内容中有;
        sql = sql.strip()
        if sql.count(";") > 1:
            sql = re.sub(r";\s?select", ";  select", sql, flags=re.I)
            sql = re.sub(r";\s?update", ";  update", sql, flags=re.I)
            sql = re.sub(r";\s?delete", ";  delete", sql, flags=re.I)
            sql = re.sub(r";\s?insert", ";  insert", sql, flags=re.I)
            sql = re.sub(r";\s?replace", ";  replace", sql, flags=re.I)
            sql = re.sub(r";\s?alter", ";  alter", sql, flags=re.I)
            sql = re.sub(r";\s?drop", ";  drop", sql, flags=re.I)
            sql = re.sub(r";\s?create", ";  create", sql, flags=re.I)
            #
            # idx = sql.find(';  ')
            ##if idx != -1 and idx != len(sql)-1:
            sqlList = sql.split(";  ")
            sqlList = filter(None, sqlList)  # 去除空值
            sqlList = list(sqlList)
            #
            lenList = len(sqlList)
            for i in range(0, lenList - 1):  # 留最后一个
                sql = sqlList[i] + ";"
                ret, result = self._exec_sql_normal(sql)
            # 最后一条
            # sql = sqlList[-1] +';'
            sql = sqlList[-1]
        else:
            pass
        #
        # if not limit == 0:
        #    sql = self.sqlAppendLimit(sql, limit)
        #
        ret, result = self._exec_sql_normal(sql)
        #
        return ret, result

    # -1 失败
    # 0 结果为空
    # 1 结果为1到多条
    def _exec_sql_normal(self, sql):
        # self.logger.info("send sql:\n%s" % ( sql))
        try:
            n = self.cur.execute(sql)
            self.conn.commit()
            #
            affect_rows = self.cur.rowcount
            self.logger.info("affect_rows: %d," % affect_rows)
            ret = affect_rows
            #
            rows = self.cur.fetchall()
            rows = list(rows)
            # print rows
            #
            if n == 0:
                ret = 0
            else:
                if self.cur.description:  # 字段次序
                    colNameList = [tuple[0] for tuple in self.cur.description]
                # ret = 1

            #
            sortListRows = []
            # 时间转换'FmodifyTime': datetime.datetime(2018, 6, 19, 14, 54, 29)
            # 时间转换'Fdate': datetime.date(2018, 6, 19)
            lRows = len(rows)
            for i in range(0, lRows):
                for k1, v1 in rows[i].items():
                    if type(v1) == datetime.datetime:
                        # self.logger.info("cng field:%s"%str(v1))
                        rows[i][k1] = v1.strftime("%Y-%m-%d %H:%M:%S")
                    elif type(v1) == datetime.date:
                        rows[i][k1] = v1.strftime("%Y-%m-%d")
                    elif (
                            type(v1) == Decimal
                    ):  # TypeError: Decimal('0') is not JSON serializable
                        # self.logger.info("cng field:%s" % str(v1))
                        rows[i][k1] = float(v1)
                    else:
                        pass
                #
                # 把字段按创建表的字段排下序
                dictRow = OrderedDict()
                for k in colNameList:
                    dictRow[k] = rows[i][k]
                #
                sortListRows.append(dictRow)
            #
            if sortListRows:
                # print "sortListRows>>",sortListRows
                # result = pickle.dumps(sortListRows)
                result = json.dumps(sortListRows)
            else:
                # result = str(rows)
                # result = pickle.dumps(rows)
                result = json.dumps(rows)
            #
            if lRows > 0:
                if lRows <= 2:
                    self.logger.debug("tuple size n:%d,result:\n%s" % (n, result))
                else:
                    self.logger.debug("tuple size n:%d,row 0 :%s" % (n, str(rows[0])))
        except Exception as e:
            ret = -1
            result = str(e)
            self.logger.error("sql:\n%s\n,result:%s" % (sql, result))
            # logging.info(repr(e))
            self.logger.error("\n%s" % traceback.format_exc())
            self.closeDb()
        #
        # if result=='()':
        #    result=''
        # print result
        return ret, result

    def query_record(self, db_con, query_sql):
        # logger.info("query sql: %s" % query_sql)
        # 使用cursor()方法获取操作游标
        cursor = db_con.cursor()
        try:
            # 执行SQL语句
            cursor.execute(query_sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            return results
        except Exception as e:
            self.logger.error("Error: unable to fecth data %s" % str(e))

    def exec_db_sql(self, db_con, sql):
        # logger.info("exec sql : %s" % sql)
        # 使用cursor()方法获取操作游标
        cursor = db_con.cursor()

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db_con.commit()
        except Exception as e:
            # 发生错误时回滚
            db_con.rollback()

    # DB连接
    def connect_db(self, db_name):
        # print "连接DB..."
        self.logger.info("connecct DB...")

        db_con = pymysql.connect(
            self.ip, self.user, self.passwd, db_name, charset="utf8"
        )
        self.logger.info("db_host: %s" % self.ip)

        # print "DB连接成功!"
        self.logger.info("success to connecct!")
        return db_con

    def close_db(self, db_con):
        self.logger.info("close db!")
        db_con.close()

    # #自己从配置查找ip
    # def exec_sql_conn(self, sql,dictPara):
    #     import db_getEnvIp
    #     # dictPara['tbType']='settle'
    #     # tbMark = dictPara['tbMark']='c2c_settlement' #一般是db名除非有不同ip
    #     # dictPara['setFind']='51445' #具体值比如uid的值等，用来找核心多set的ip port
    #     ipDict=db_getEnvIp.get_db_cfg(dictPara)
    #     self.connectDb(ipDict)
    #     ret, result = self.exec_sql(sql)
    #     self.closeDb()
    #     return ret, result


# [OrderedDict([(u'Fid', 281),(u'Fbatch_no', u'201807241727582000014583'),
#
# SELECT Fspid  from c2c_db.t_merchant_info where Fspid='1383881002'

if __name__ == "__main__":
    pass
    # ip = '10.125.54.139'
    # user = 'root'
    # passwd = 'root1234'
    # port = '3306'
    # #
    # sqlExec = MySqlExec(ip, user, passwd, port)
    # sqlExec.connectDb()
    # sql = "select * from isp_settle_db.t_cb_rmb_detail_201806"
    # ret, result = sqlExec.exec_sql(sql)
    # #
    # listDict = json.loads(result, object_pairs_hook=OrderedDict)
    # print(listDict)
    # # print "0>>",listDict[0]['Fid']
    # # print "1>>",listDict[1]
    # sqlExec.closeDb()

    #
    # 通过TestObj/settle/api/db.json中获取ip
    # sqlExec = MySqlExec()
    # sql = "delete from isp_merchant_db.t_refund_sum where Frefund_batchid='201807030002'; "
    # dictPara={}
    # dictPara['tbType']='settle'
    # dictPara['tbMark'] = 'isp_merchant_db'
    # sqlExec.exec_sql_conn(sql,dictPara)
