#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: FastAPIDemo
    @File： inspect_db.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/13 09:50
    @Desc: 
================================================="""
import os
import sqlalchemy
from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlmodel import SQLModel, Field
from typing import List, Optional
import re


def get_table_columns(engine, table_name):
    """从数据库获取表的列信息，包括字段注释和其他属性"""
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    for column in columns:
        # 获取列的注释，若没有则默认为空字符串
        column['comment'] = column.get('comment', '')
        # 获取列的最大长度（对于字符串类型的字段）
        column['max_length'] = None
        if isinstance(column['type'], sqlalchemy.types.String):
            column['max_length'] = column['type'].length
    return columns


def get_pydantic_field_type(column_type: str):
    """根据数据库字段类型返回SQLModel字段类型"""
    if 'INTEGER' in column_type:
        return int
    elif 'VARCHAR' in column_type or 'TEXT' in column_type:
        return str
    elif 'BOOLEAN' in column_type:
        return bool
    elif 'DATE' in column_type:
        return str  # 可以使用 `datetime.date` 来处理日期
    elif 'FLOAT' in column_type or 'DECIMAL' in column_type:
        return float
    return str


def create_sqlmodel_model(table_name: str, columns: List[dict]) -> str:
    """根据数据库表结构生成SQLModel模型类"""
    model_name = re.sub(r"(\w)([A-Z])", r"\1_\2", table_name).lower().capitalize()
    class_def = f"class {model_name.upper()}(SQLModel, table=True):\n"

    for column in columns:
        column_name = column['name']
        column_type = str(column['type'])
        pydantic_type = get_pydantic_field_type(column_type)
        column_comment = column.get('comment', '')
        max_length = column.get('max_length')

        # 处理字段是否为可选（NULLABLE）
        is_nullable = column['nullable']
        field_type = Optional[pydantic_type] if is_nullable else pydantic_type

        # 如果有注释，作为description传入
        description = f"'{column_comment}'" if column_comment else "''"

        # 如果字段有最大长度，作为max_length传入
        field_args = f"None, description={description}, sa_column_kwargs={{'comment': {description}}}"
        if max_length:
            field_args = f"None, max_length={max_length}, description={description}, sa_column_kwargs={{'comment': {description}}}"

        class_def += f"    {column_name}: {field_type} = Field({field_args})\n"
    return class_def


def generate_models_from_db(database_url: str, output_file: str):
    """从数据库生成 SQLModel 模型并保存到同一个文件"""
    # 连接数据库
    engine = create_engine(database_url)
    metadata = MetaData()

    # 获取所有表
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    # 创建输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入必要的导入语句
        f.write("from sqlmodel import SQLModel, Field\n\n")

        # 生成模型
        for table_name in tables:
            columns = get_table_columns(engine, table_name)

            # 生成 SQLModel 模型类
            sqlmodel_class = create_sqlmodel_model(table_name, columns)

            # 将 SQLModel 模型写入同一个文件
            f.write(sqlmodel_class + "\n\n")

    print(f"所有模型已成功生成并保存到文件: {output_file}")


if __name__ == "__main__":
    # 数据库连接 URL (根据实际情况修改)
    from database import DATABASE_URL
    OUTPUT_FILE = "all_models.py"

    generate_models_from_db(DATABASE_URL, OUTPUT_FILE)
