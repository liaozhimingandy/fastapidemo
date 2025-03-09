#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: FastAPIDemo
    @File： models.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/19 08:55
    @Desc: 
=================================================
"""
from enum import Enum
import uuid
from datetime import datetime

from sqlalchemy.dialects.mysql import SMALLINT
from sqlmodel import SQLModel, Field

TABLE_PREFIX = "chat"


class CHAT_POST(SQLModel, table=True):
    """
    帖子模型
    """

    __tablename__ = f"{TABLE_PREFIX}_post"  # 表名
    __table_args__ = {'comment': '帖子'}  # 表备注

    class RightStatusEnum(Enum):
        """帖子权限"""

        PUBLIC = 1
        PRIVATE = 2

        @property
        def label(self):
            mapping = {
                1: "公开",
                2: "仅自己"
            }
            return mapping[self.value]

    class FromDeviceEnum(Enum):
        """设备来源类型"""

        WEB = 1
        ANDROID = 2
        IOS = 3
        UNKNOWN = 9

        @property
        def label(self):
            mapping = {
                1: "网页版",
                2: "安卓端",
                3: "IOS",
                9: "未知"
            }
            return mapping[self.value]

    class ContentClassEnum(Enum):
        """内容类型"""
        TextElem = 1

        @property
        def label(self):
            mapping = {
                1: "普通"
            }
            return mapping[self.value]

    id: int = Field(None, primary_key=True, description='表主键ID', sa_column_kwargs={'comment': '表主键ID'})
    post_id: uuid = Field(default_factory=uuid.uuid4, index=True, description='帖子ID',
                          sa_column_kwargs={'comment': '帖子ID'})
    content: str = Field(None, description='内容', max_length=1024, sa_column_kwargs={'comment': '内容'})
    account_id: str = Field(..., index=True, max_length=32, description='用户ID', sa_column_kwargs={'comment': '用户ID'})
    from_ip: str = Field(None, description='来源ip',  max_length=32, sa_column_kwargs={'comment': '来源ip'})
    from_device: FromDeviceEnum = Field(sa_type=SMALLINT, description='来源设备名称',
                                        sa_column_kwargs={'comment': '来源设备名称'})
    right_status: RightStatusEnum = Field(sa_type=SMALLINT, description='权限状态',
                                          sa_column_kwargs={'comment': '权限状态'})
    location: str | None = Field(None, max_length=64, description='位置', sa_column_kwargs={'comment': '位置'})
    is_top: bool = Field(default=False, description='是否置顶', sa_column_kwargs={'comment': '是否置顶'})
    content_class: ContentClassEnum = Field(sa_type=SMALLINT, description='内容类型', sa_column_kwargs={'comment': '内容类型'})
    latitude: str | None = Field(None, description='经度', sa_column_kwargs={'comment': '经度'})
    longitude: str | None = Field(None, description='纬度', sa_column_kwargs={'comment': '纬度'})
    status: int = Field(None, description='帖子状态', sa_column_kwargs={'comment': '帖子状态'})
    gmt_created: datetime = Field(default_factory=datetime.now, description='创建日期时间',
                                  sa_column_kwargs={'comment': '创建日期时间'})


class CHAT_COMMENT(SQLModel, table=True):
    """
    评论模型
    """

    __tablename__ = f"{TABLE_PREFIX}_comment"  # 表名
    __table_args__ = {'comment': '评论'}  # 表备注

    id: int = Field(None, primary_key=True, description='表主键ID', sa_column_kwargs={'comment': '表主键ID'})
    comment_id: uuid = Field(default_factory=uuid.uuid4,  index=True, description='评论ID',
                             sa_column_kwargs={'comment': '评论ID'})
    is_root: bool = Field(False, description='是否为一级评论', sa_column_kwargs={'comment': '是否为一级评论'})
    parent_id: str | None = Field(None, description='父评论', max_length=32, sa_column_kwargs={'comment': '父评论'})
    content: str = Field(None, description='评论内容', max_length=255, sa_column_kwargs={'comment': '评论内容'})
    account_id: str = Field(None,  index=True, max_length=32, description='评论者', sa_column_kwargs={'comment': '评论者'})
    post_id: str = Field(..., index=True, description='评论对象ID',  max_length=32, sa_column_kwargs={'comment': '评论对象ID'})
    gmt_created: datetime = Field(default_factory=datetime.now, description='创建日期时间',
                                  sa_column_kwargs={'comment': '创建日期时间'})


class CHAT_LIKE(SQLModel, table=True):
    """
    赞模型
    """

    __tablename__ = f"{TABLE_PREFIX}_like"  # 表名
    __table_args__ = {'comment': '赞'}  # 表备注

    id: int = Field(None, primary_key=True, description='表主键ID', sa_column_kwargs={'comment': '表主键ID'})
    post_id: str = Field(None, index=True, description='赞对象ID', sa_column_kwargs={'comment': '赞对象ID'})
    account_id: str = Field(...,  index=True, max_length=32, description='点赞的用户', sa_column_kwargs={'comment': '点赞的用户'})
    gmt_created: datetime = Field(default_factory=datetime.now, description='创建日期时间',
                                  sa_column_kwargs={'comment': '创建日期时间'})


class CHAT_IMAGE(SQLModel, table=True):
    """
    上传文件图片模型
    """

    __tablename__ = f"{TABLE_PREFIX}_image"  # 表名
    __table_args__ = {'comment': '图片'}  # 表备注

    id: int = Field(None, primary_key=True, description='表主键ID', sa_column_kwargs={'comment': '表主键ID'})
    image_name: str = Field(..., max_length=128, description='图片名称', sa_column_kwargs={'comment': '图片名称'})
    image_url: str = Field(..., max_length=128, description='图片url', sa_column_kwargs={'comment': '图片url'})
    image_md5: str = Field(...,  max_length=32, description='图片md值', sa_column_kwargs={'comment': '图片md值'})
    gmt_created: datetime = Field(None, description='', sa_column_kwargs={'comment': '创建日期时间'})

