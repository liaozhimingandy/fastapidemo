#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: django_hip_service
    @File： cda.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2024-10-09 9:23
    @Desc: cda导出工具类
=================================================
"""
import asyncio

import pandas as pd
import pyodbc

cda_map = {
    'C0001': '病历概要',
    'C0002': '门（急）诊病历',
    'C0003': '急诊留观病历',
    'C0004': '西药处方',
    'C0005': '中药处方',
    'C0006': '检查报告',
    'C0007': '检验报告',
    'C0008': '治疗记录',
    'C0009': '一般手术记录',
    'C0010': '麻醉术前访视记录',
    'C0011': '麻醉记录',
    'C0012': '麻醉术后访视记录',
    'C0013': '输血记录',
    'C0014': '待产记录',
    'C0015': '阴道分娩记录',
    'C0016': '剖宫产记录',
    'C0017': '一般护理记录',
    'C0018': '病重（病危）护理记录',
    'C0019': '手术护理记录',
    'C0020': '生命体征测量记录',
    'C0021': '出入量记录',
    'C0022': '高值耗材使用记录',
    'C0023': '入院评估',
    'C0024': '护理计划',
    'C0025': '出院评估与指导',
    'C0026': '手术知情同意书',
    'C0027': '麻醉知情同意书',
    'C0028': '输血治疗同意书',
    'C0029': '特殊检查及特殊治疗同意书',
    'C0030': '病危（重）通知书',
    'C0031': '其他知情告知同意书',
    'C0032': '住院病案首页',
    'C0033': '中医住院病案首页',
    'C0034': '入院记录',
    'C0035': '24小时内入出院记录',
    'C0036': '24小时内入院死亡记录',
    'C0037': '首次病程记录',
    'C0038': '日常病程记录',
    'C0039': '上级医师查房记录',
    'C0040': '疑难病例讨论记录',
    'C0041': '交接班记录',
    'C0042': '转科记录',
    'C0043': '阶段小结',
    'C0044': '抢救记录',
    'C0045': '会诊记录',
    'C0046': '术前小结',
    'C0047': '术前讨论',
    'C0048': '术后首次病程记录',
    'C0049': '出院记录',
    'C0050': '死亡记录',
    'C0051': '死亡病例讨论记录',
    'C0052': '住院医嘱',
    'C0053': '出院小结'
}


class CDATool(object):

    def __init__(self, ip='localhost', dbname='CDADB', user='caradigm', password='Knt2020@lh', port="1433"):
        self.ip = ip
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None

    def get_cursor(self):
        try:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={self.ip};'
                f'DATABASE={self.dbname};'
                f'UID={self.user};'
                f'PWD={self.password}',
                timeout=3
            )  # 获取连接

        except(Exception,) as e:
            return None
        else:
            return self.conn.cursor()

    # 异步函数封装
    async def get_db_cursor_async(self):
        """
        将同步函数封装成异步函数,避免阻塞执行线程

        Returns:
            协程

        """
        loop = asyncio.get_event_loop()
        # 将阻塞操作提交到线程池中执行
        # func必须为函数,不能为协程对象
        result = await loop.run_in_executor(None, self.get_cursor)
        return result

    def __del__(self):
        if self.conn:
            self.conn.close()

    @classmethod
    def collect_data_to_csv(cls, data: dict, file_name='') -> None:
        list_cda_collect_data = []
        for item in cda_map.items():
            list_cda_collect_data.append((item[0], item[1], data.get(item[0], 0)))

        name = ['文档类型代码', '文档类型名称', '文档数量']
        df = pd.DataFrame(columns=name, data=list_cda_collect_data)

        df.to_excel(f'统计数据-{file_name}.xlsx')


def query_to_dict(cursor) -> list:
    """
    将查询数据集转成字典数据集

    Args:
        cursor: 数据库操作游标

    Returns:
        List: 返回列表,列表里的元素为字典
    """
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]



if __name__ == "__main__":
    pass
