# -*- coding:utf-8 -*-
# Copyright (C) 2018 All rights reserved.
#
# @File conf.py
# @Brief
# @Author abelzhu, abelzhu@tencent.com
# @Version 1.0
# @Date 2018-02-23
 
# 设置为true会打印一些调试信息
DEBUG = True


# 企业微信的一些配置项
Conf = {
    # 企业的id，在管理端->"我的企业" 可以看到
    "CORP_ID": "ww0f3efc2873ad11c3",

    # "通讯录同步"应用的secret, 开启api接口同步后，可以在管理端->"通讯录同步"看到
    "CONTACT_SYNC_SECRET": "xWPfryWX7Fv1BcJSpivflpPQXC_v5iH0HY2zfu1soTA",

    # 运维组ID
    "OPS_DEP_ID": '346',

    # 某个自建应用的id及secret, 在管理端 -> 企业应用 -> 自建应用, 点进相应应用可以看到
    "APP_ID": '1000078',
    "APP_SECRET": "7MHpdQICiegx9rIc4iZrEPunb1aYUqdJYKSW9v7a1A8",

    # 打卡应用的 id 及secrete， 在管理端 -> 企业应用 -> 基础应用 -> 打卡，
    # 点进去，有个"api"按钮，点开后，会看到
    "CHECKIN_APP_ID": 0,
    "CHECKIN_APP_SECRET": "",

    # 审批应用的 id 及secrete， 在管理端 -> 企业应用 -> 基础应用 -> 审批，
    # 点进去，有个"api"按钮，点开后，会看到
    "APPROVAL_APP_ID": 0,
    "APPROVAL_APP_SECRET": "",
}
