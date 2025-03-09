#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: FastAPIDemo
    @File： models.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/19 09:19
    @Desc: 
=================================================
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy.dialects.mysql import SMALLINT
from sqlmodel import SQLModel, Field


TABLE_PREFIX = "account"

def uuid_generator(size: int = 7):
    return uuid.uuid4().hex[:size]

def salt_default():
    """盐默认生成"""
    return uuid_generator(8)


def userid_default():
    """用户id随机生成"""
    return uuid_generator(7)


def app_id_default():
    """应用id随机生成"""
    return uuid_generator(5)


class ACCOUNT(SQLModel, table=True):
    """
    账户信息模型
    """

    __tablename__ = f"{TABLE_PREFIX}_account"  # 表名
    __table_args__ = {'comment': '帖子'}  # 表备注

    class SexEnum(Enum):
        UnKnown = 0
        Female = 1
        Male = 2
        Other = 9

        @property
        def label(self):
            mapping = {
                0: "未知的性别",
                1: "男性",
                2: "女性",
                9: "未说明的性别"
            }
            return mapping[self.value]

    class AreaCodeEnum(Enum):
        CHN = ('CHN', '中国')

        @property
        def label(self):
            mapping = {
                'CHN': "中国"
            }
            return mapping[self.value]


    id: int = Field(None, primary_key=True, description='表主键ID', sa_column_kwargs={'comment': '表主键ID'})
    account_id: str = Field(default=userid_default, index=True, max_length=32,
                            description='用户ID', sa_column_kwargs={'comment': '用户ID'})
    username: str = Field(None,  index=True, max_length=7, description='用户名', sa_column_kwargs={'comment': '用户名'})
    nick_name: str = Field(None, max_length=64, description='昵称', sa_column_kwargs={'comment': '昵称'})
    email: str | None = Field(None, index=True, max_length=254, description='电子邮箱', sa_column_kwargs={'comment': '电子邮箱'})
    gmt_birth: datetime | None = Field(None, description='出生日期', sa_column_kwargs={'comment': '出生日期'})
    areaCode: AreaCodeEnum = Field(default=AreaCodeEnum.CHN, max_length=5, description='区域代码',
                                   sa_column_kwargs={'comment': '区域代码'})
    mobile: str | None = Field(None, index=True, max_length=32, description='电话号码', sa_column_kwargs={'comment': '电话号码'})
    sex: SexEnum = Field(default=SexEnum.UnKnown,  sa_type=SMALLINT, description='性别', sa_column_kwargs={'comment': '性别'})
    avatar: str = Field(None, max_length=200, description='头像链接', sa_column_kwargs={'comment': '头像链接'})
    is_active: bool = Field(default=True, description='账户状态', sa_column_kwargs={'comment': '账户状态'})
    user_type: int = Field(default=1, sa_type=SMALLINT, description='账户类型', sa_column_kwargs={'comment': '账户类型'})
    password: str | None = Field(None, max_length=128, description='用户密码', sa_column_kwargs={'comment': '用户密码'})
    allow_add_friend: bool = Field(default=True, description='允许添加好友', sa_column_kwargs={'comment': '允许添加好友'})
    allow_beep: bool = Field(default=True, description='是否允许提示音', sa_column_kwargs={'comment': '是否允许提示音'})
    allow_vibration: bool = Field(default=True, description='是否允许震动提示', sa_column_kwargs={'comment': '是否允许震动提示'})
    gmt_created: datetime = Field(default_factory=datetime.now, description='创建日期时间',
                                  sa_column_kwargs={'comment': '创建日期时间'})
    im_id: str | None = Field(None, max_length=64, description='im ID', sa_column_kwargs={'comment': 'im ID'})
    salt: str = Field(default=salt_default, max_length=8, description='盐', sa_column_kwargs={'comment': '盐'})
    gmt_modified: datetime = Field(default_factory=datetime.now, description='最后修改时间',
                                   sa_column_kwargs={'comment': '最后修改时间'})


class APP(SQLModel, table=True):
    """
    应用模型
    示例: 小程序,公众号...
    """

    __tablename__ = f"{TABLE_PREFIX}_app"  # 表名
    __table_args__ = {'comment': '应用'}  # 表备注

    id: int = Field(None, primary_key=True, description='表主键ID', sa_column_kwargs={'comment': '表主键ID'})
    app_id: str = Field(default=app_id_default, index=True, max_length=7,
                        description='appid', sa_column_kwargs={'comment': 'appid'})
    app_secret: str = Field(..., max_length=32, description='应用密钥', sa_column_kwargs={'comment': '应用密钥'})
    salt: str = Field(default=salt_default, max_length=8, description='盐',
                      sa_column_kwargs={'comment': '盐'})
    app_name: str = Field(..., max_length=32, description='应用名称', sa_column_kwargs={'comment': '应用名称'})
    app_en_name: str | None = Field(None, max_length=64, description='应用英文名称',
                                    sa_column_kwargs={'comment': '应用英文名称'})
    is_active: bool = Field(default=True, description='激活状态', sa_column_kwargs={'comment': '激活状态'})
    gmt_created: datetime = Field(default_factory=datetime.now, description='创建日期时间',
                                  sa_column_kwargs={'comment': '创建日期时间'})
    gmt_updated: datetime = Field(default_factory=datetime.now, description='最后更新日期时间',
                                  sa_column_kwargs={'comment': '最后更新日期时间'})