test_download_param = {
    "url": 'http://106.52.209.84:12347/api/download',
    "user_name": "test_download_0618_21",
    "downd_param": [
        # 单一url与空路径
        {
            "case_name": "单一url与空路径",
            "url_list": [
                "http://contentcms-bj.cdn.bcebos.com/cmspic/56818dff650d849593196f2258a638b3.jpeg"
                ],
            "local_path": "",
            "db_bf_ret": 0, # 0表示sql执行成功 满足条件条数为0 -1表示sql执行失败 1表示满足条件不为0
            "request_code": 200,
            "request_ret": 0, # 0表示成功或者部分url下载成功 1表示失败
            "db_write_ret": 1, # 查询db满足条件数量 1为写入1条 0为未写入
            "db_cfm_ret": 0, # 查询表中标志位
            "db_del_dd_ret": 1, # 删除download_detail表 ret删除后为0
            "db_del_dd_result": "[]", # 删除download_detail表 result删除后为"[]"
            "db_del_opn_ret": 1, # 删除operation表 ret删除后为0
            "db_del_opn_result": "[]", # 删除operation表 result删除后为"[]"
            "db_del_n2i_ret": 1, # 删除name2id表 ret删除后为0
            "db_del_n2i_result": "[]", # 删除name2id表 result删除后为"[]"
        },
        # 多个正确url与空路径
        {
            "case_name": "多个url与空路径",
            "url_list": [
                "http://contentcms-bj.cdn.bcebos.com/cmspic/56818dff650d849593196f2258a638b3.jpeg",
                "http://contentcms-bj.cdn.bcebos.com/cmspic/23683a1dfdb6536af5909ba6a931cf09.jpeg",
                "http://contentcms-bj.cdn.bcebos.com/cmspic/f5b2846807e448d267259c95720be68f.jpeg"
                ],
            "local_path": "",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,
            "db_write_ret": 1,
            "db_cfm_ret": 0,
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 单个url与相对路径
        {
            "case_name": "单个url与相对路径",
            "url_list": [
                "http://contentcms-bj.cdn.bcebos.com/cmspic/56818dff650d849593196f2258a638b3.jpeg"
            ],
            "local_path": "./",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,
            "db_write_ret": 1,
            "db_cfm_ret": 0,
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 单个url与绝对路径
        {
            "case_name": "单个url与绝对路径",
            "url_list": [
                "http://contentcms-bj.cdn.bcebos.com/cmspic/56818dff650d849593196f2258a638b3.jpeg"
            ],
            "local_path": "/home/chenlai/download_file/",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,
            "db_write_ret": 1,
            "db_cfm_ret": 0,
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 错误url与空路径
        {
            "case_name": "错误url与空路径",
            "url_list": [
                "http://contentcms-bj.cdn.bcebos.com/abcdwrong.jpg"
                ],
            "local_path": "",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 1,  # chg
            "db_write_ret": 1,
            "db_cfm_ret": 1,  # chg
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 单一url与错误路径
        {
            "case_name": "单一url与错误路径",
            "url_list": [
                "http://contentcms-bj.cdn.bcebos.com/cmspic/56818dff650d849593196f2258a638b3.jpeg"
                ],
            "local_path": "/home/chenlai/wrong/download_file/",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 1,  # chg
            "db_write_ret": 1,
            "db_cfm_ret": 1,  # chg
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 多个url部分正确与空路径
        {
            "case_name": "多个url部分正确与空路径",
            "url_list": [
                "http://contentcms-bj.cdn.bcebos.com/cmspic/56818dff650d849593196f2258a638b3.jpeg",
                "http://contentcms-bj.cdn.bcebos.com/cmspic/23683a1dfdb6536af5909ba6a931cf09.jpeg",
                "http://contentcms-bj.cdn.bcebos.com/abcdwrong.jpg",
                "http://contentcms-bj.cdn.bcebos.com/cmspic/f5b2846807e448d267259c95720be68f.jpeg"
                ],
            "local_path": "",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,
            "db_write_ret": 1,
            "db_cfm_ret": 0,
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 空url与空路径
        {
            "case_name": "空url与空路径",
            "url_list": [
                ],
            "local_path": "",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 1,  # chg
            "db_write_ret": 1,
            "db_cfm_ret": 1,  # chg
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
    ]
}


test_runcmd_param = {
    "url": 'http://106.52.209.84:12347/api/runCmd',
    "user_name": "test_runCmd_0618_21",
    "runcmd_param": [
        # 正确单一cmd命令 有返回结果
        {
            "case_name": "正确单一cmd命令 有返回结果",
            "cmd": "ls",
            "timeout": "",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,
            "return_msg": 1,  # 1表示有返回结果  0表示无返回结果
            "db_write_ret": 1,
            "db_cfm_ret": 0,
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 正确单一cmd命令 无返回结果
        {
            "case_name": "正确单一cmd命令 无返回结果",
            "cmd": "cd",
            "timeout": "",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,
            "return_msg": 0,  # 1表示有返回结果  0表示无返回结果
            "db_write_ret": 1,
            "db_cfm_ret": 0,
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 正确复合cmd命令 无返回结果
        {
            "case_name": "正确复合cmd命令 无返回结果",
            "cmd": "mkdir tt && rm -rf tt",
            "timeout": "",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,
            "return_msg": 0,  # 1表示有返回结果  0表示无返回结果
            "db_write_ret": 1,
            "db_cfm_ret": 0,
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 错误cmd命令
        {
            "case_name": "错误cmd命令 无返回结果",
            "cmd": "llcd",
            "timeout": "",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 1,  # 错误cmd命令 返回标志位为1
            "return_msg": 0,
            "db_write_ret": 1,
            "db_cfm_ret": 1,  # 与request_ret保持同步
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 执行时间极短下判断超时情况
        {
            "case_name": "执行时间极短下判断超时情况",
            "cmd": "sleep 5",
            "timeout": "2",
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 1,  # 错误cmd命令 返回标志位为1
            "return_msg": 0,
            "db_write_ret": 1,
            "db_cfm_ret": 1,  # 与request_ret保持同步
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
    ]

}


test_history_param = {
    "url": 'http://106.52.209.84:12347/api/history',
    "user_name": "test_history_0619_5",
    "history_param": [
        # 默认查询 无条件过滤
        {
            "case_name": "默认查询 无条件过滤",
            "operator": "",
            "operation": ["download", "shell", "sql"],
            "oprntime": {
                "start_time": "",  # 输入格式 "1900-01-01 00:00:00"
                "end_time": ""
            },
            "ret": "", # 0表示执行操作成功的记录 1表示执行操作失败的记录
            "limit": 10,
            "offset": 0,
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,  # 正确为0 错误为1
            "db_write_ret": 1,
            "db_cfm_ret": 0,  # 与request_ret保持同步
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 查询download成功的记录
        {
            "case_name": "查询download成功的记录",
            "operator": "",
            "operation": ["download"],
            "oprntime": {
                "start_time": "",
                "end_time": ""
            },
            "ret": "0",
            "limit": 10,
            "offset": 0,
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,  # 正确为0 错误为1
            "db_write_ret": 1,
            "db_cfm_ret": 0,  # 与request_ret保持同步
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 查询该时间段内无记录的返回
        {
            "case_name": "查询该时间段内无记录的返回",
            "operator": "",
            "operation": ["download"],
            "oprntime": {
                "start_time": "1900-01-01 00:00:00",
                "end_time": "1900-01-01 00:00:01"
            },
            "ret": "0",
            "limit": 10,
            "offset": 0,
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,  # 正确为0 错误为1
            "db_write_ret": 1,
            "db_cfm_ret": 0,  # 与request_ret保持同步
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 查询时间段只包含起始时间
        {
            "case_name": "查询时间段只包含起始时间",
            "operator": "",
            "operation": ["download"],
            "oprntime": {
                "start_time": "2021-06-18 00:00:00",
                "end_time": ""
            },
            "ret": "0",
            "limit": 10,
            "offset": 0,
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,  # 正确为0 错误为1
            "db_write_ret": 1,
            "db_cfm_ret": 0,  # 与request_ret保持同步
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        },
        # 查询总条数之外的分页数据
        {
            "case_name": "查询总条数之外的分页数据",
            "operator": "",
            "operation": ["download"],
            "oprntime": {
                "start_time": "",
                "end_time": ""
            },
            "ret": "0",
            "limit": 10,
            "offset": 10000,
            "db_bf_ret": 0,
            "request_code": 200,
            "request_ret": 0,  # 正确为0 错误为1
            "db_write_ret": 1,
            "db_cfm_ret": 0,  # 与request_ret保持同步
            "db_del_dd_ret": 1,
            "db_del_dd_result": "[]",
            "db_del_opn_ret": 1,
            "db_del_opn_result": "[]",
            "db_del_n2i_ret": 1,
            "db_del_n2i_result": "[]",
        }
    ]
}