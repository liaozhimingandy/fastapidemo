#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: FastAPIDemo
    @File： hiptools.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/4 09:45
    @Desc: 
================================================="""
import asyncio
import os
import shutil
import uuid
import time
import zipfile
from types import NoneType
from typing import Optional, List

from strawberry import Info
from typing_extensions import Annotated, Doc
import strawberry
from strawberry.fastapi import GraphQLRouter
from lxml import etree as et

from fastapidemo.utils import CDATool, query_to_dict, cda_map

# 定义XML命名空间
namespace = {'xmlns': 'urn:hl7-org:v3'}


async def update_demo_param(service: str, dir_name: str, *args) -> None:
    """
    更新示例参数

    Args:
        service: 服务代码
        dir_name: 生成的目录
        args: 参数列表,需要更新的xml节点列表

    Returns:
        返回None

    """
    list_file_path = {
        "PatientInfoQuery": "EMR-PL-04-个人信息查询服务",
        "OrganizationInfoQuery": "EMR-PL-07-医疗卫生机构（科室）信息查询服务",
        "ProviderInfoQuery": "EMR-PL-10-医疗卫生人员信息查询服务",
        "TerminologyQuery": "EMR-PL-13-术语查询服务",
        "DocumentAccess": "EMR-PL-15-电子病历文档检索服务",
        "DocumentRetrieve": "EMR-PL-16-电子病历文档调阅服务",
        "EncounterCardInfoQuery": "EMR-PL-19-就诊卡信息查询服务",
        "SourceAndScheduleInfoQuery": "EMR-PL-52-号源排班信息查询服务",
        "OutPatientInfoQuery": "EMR-PL-22-门诊挂号信息查询服务",
        "InPatientInfoQuery": "EMR-PL-25-住院就诊信息查询服务",
        "TransferInfoQuery": "EMR-PL-28-住院转科信息查询服务",
        "DischargeInfoQuery": "EMR-PL-31-出院登记信息查询服务",
        "OrderInfoQuery": "EMR-PL-34-医嘱信息查询服务",
        "ExamAppInfoQuery": "EMR-PL-37-检验申请信息查询服务",
        "CheckAppInfoQuery": "EMR-PL-40-检查申请信息查询服务",
        "PathologyAppInfoQuery": "EMR-PL-43-病理申请信息查询服务",
        "BloodTransAppInfoQuery": "EMR-PL-46-输血申请信息查询服务",
        "OperationAppInfoQuery": "EMR-PL-49-手术申请信息查询服务",
        "OutPatientAppointStatusInfoQuery": "EMR-PL-55-门诊预约状态信息查询服务",
        "CheckAppointStatusInfoQuery": "EMR-PL-58-检查预约状态信息查询服务",
        "OrderFillerStatusInfoQuery": "EMR-PL-60-医嘱执行状态信息查询服务",
        "CheckStatusInfoQuery": "EMR-PL-62-检查状态信息查询服务",
        "ExamStatusInfoQuery": "EMR-PL-64-检验状态信息查询服务",
        "OperationScheduleInfoQuery": "EMR-PL-79-手术排班信息查询服务",
        "OperationStatusInfoQuery": "EMR-PL-81-手术状态信息查询服务"
    }
    assert len(args) > 0, "No arguments"
    id_msg = str(uuid.uuid4())
    gmt_created = time.strftime('%Y%m%d%H%M%S')

    id_sender, id_receiver = os.getenv('SEND_ID', 'esbid_send'), os.getenv('RECV_ID', 'esbid_receive')

    file_name_t, file_name_f = f"{list_file_path[service]}-T01.xml", f"{list_file_path[service]}-F01.xml"

    for file_name in [file_name_t, file_name_f]:
        doc = et.parse(os.path.join("static/services", file_name))
        root = doc.getroot()

        # 公共基本信息修改
        root.find('xmlns:id', namespace).set('extension', id_msg)
        root.find('xmlns:creationTime', namespace).set('value', gmt_created)
        root.find('xmlns:sender/xmlns:device/xmlns:id/xmlns:item', namespace).set('extension', id_sender)
        root.find('xmlns:receiver/xmlns:device/xmlns:id/xmlns:item', namespace).set('extension', id_receiver)

        for item in args:
            path, node = item.path.strip().split('/@')
            # 如何是正向测试用例则正常赋值,反向测试用例则默认赋值000000
            root.find(path, namespaces=namespace).set(node, item.value
            if file_name_t == file_name else os.getenv("DEFAULT_TEST_VALUE", '000000'))

        # 创建文件夹
        dir_path = f"static/temp/services/{dir_name}"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        result_file = f"{dir_path}/{file_name}"

        # 保存到文件
        doc.write(result_file, pretty_print=True, xml_declaration=True, encoding='UTF-8')


async def create_examples_zip(dir_name: Annotated[str, Doc("目录名称")], is_service: bool = True) -> str:
    """
    根据指定的目录名称,将该目录打包生成zip文件,并且返回压缩文件名称

    Args:
        dir_name: 打包的目录名
        is_service: 打包的目录是否是交互服务;填false则为CDA

    Returns:
        压缩文件名称

    """
    dir_path = f"static/temp/{'services' if is_service else 'cdas'}/{dir_name}"
    # 创建一个 Zip 文件
    zip_filepath = f'static/temp/archive-{'services' if is_service else 'cdas'}-{dir_name}.zip'

    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 将文件添加到 ZIP 文件中
                zipf.write(file_path, os.path.relpath(file_path, dir_path))

    # 删除原始文件夹
    shutil.rmtree(dir_path)

    return zip_filepath


@strawberry.input(description="参数信息")
class Content:
    comment: Annotated[str, Doc("备注说明")]
    eg: Annotated[Optional[str], Doc("示例")] = None
    path: Annotated[str, Doc("参数取值路径")]
    value: Annotated[str, Doc("取值")]
    sql: Annotated[Optional[str], Doc("底层sql查询语句")] = None


@strawberry.input(description="服务基本信息")
class Service:
    service_code: Annotated[str, Doc("服务代码")]
    service_name: Annotated[str, Doc("服务名称")]
    rank: Annotated[str, Doc("互联互通评测等级")]
    params: Annotated[List[Content], Doc("参数列表")]


@strawberry.input(description="输入参数")
class DataInputType:
    """
    入参数据模型
    """
    data: Annotated[List[Service], Doc("数据")]


def resolve_hello(name: Annotated[str, Doc("名称")] = None) -> str:
    """
    仅用于接口测试,根据用户输入的字符串返回数据

    Args:
        name: 任意字符串

    Returns:
        字符串

    Example usage:
        暂无

    """
    return f"你好, {name}"


@strawberry.type
class Query:

    # @strawberry.field
    # def hello(self, name: Annotated[str, Doc("名称")] = None) -> str:
    #     return f"你好, {name}"
    hello: str = strawberry.field(resolver=resolve_hello, description="仅供测试")

    @strawberry.field(description="生成交互服务测试用例")
    async def examples_services(self, data: Annotated[DataInputType, Doc("入参")], info=strawberry.Info) -> str| None:
        """
        生成交互服务测试用例

        Args:
            data: 自定义类型DataInputType
            info: 用于添加后台任务

        Returns:
            返回空字符或None

        """
        # 临时文件路径
        dir_name = str(uuid.uuid4())

        # 处理数据（这里可以根据需要处理 input_data）
        for item in data.data:
            await update_demo_param(item.service_code, dir_name, *item.params)

        # 创建后台任务执行生成zip文件
        info.context['background_tasks'].add_task(create_examples_zip, dir_name=dir_name, is_service=True)

        return f'{info.context.get('request').base_url}static/temp/archive-services-{dir_name}.zip'

    @strawberry.field(description="通过就诊流水号获取cda文档")
    async def read_cdas_by_adm_no(self, adm_no: Annotated[str, Doc("就诊流水号")], info: Optional[Info] =strawberry.Info) -> str:
        """
        根据就诊流水号导出该条件下符合条件的所有CDA并且生成xml,最后打包成zip文件供下载使用

        Args:
            adm_no: 就诊流水号
            info: 用于添加后台任务

        Returns:
            供下载使用的链接

        """
        sql = ("select [no], PatientName patient_name, DocTypeCode doc_type_code, DocContent content "
               "from(SELECT row_number() over(partition by DocTypeCode order by CreateTime asc) no, [PatientName], DocTypeCode, [DocContent] "
               "from CDADocument where Visit_id = ? ) as T where T.[no] < ?")

        cda = CDATool(ip=os.getenv("ip", '172.16.33.179'), user=os.getenv('user', 'caradigm'),
                      password=os.getenv('password', 'Knt2020@lh'), dbname=os.getenv('dbname', 'CDADB'))

        # 将同步函数封装成异步函数,防止阻塞进程
        cursor = await cda.get_db_cursor_async()
        assert not isinstance(cursor, (NoneType,)), "数据库连接失败"
        await cursor.execute(sql, (adm_no, int(os.getenv('MAX_CDA_NUM', 20))))

        # 临时文件路径
        dir_path = uuid.uuid4()
        file_dir = f'static/temp/cdas/{dir_path}'

        # 是否查询到CDA
        is_have_cda = False

        for row in query_to_dict(cursor):
            is_have_cda = True
            if not os.path.exists(file_dir):
                os.makedirs(os.path.join(file_dir, row['patient_name']))
            tmp_file_name = f'EMR-SD-{row["doc_type_code"][-2:]}-{cda_map.get(row["doc_type_code"], "未知")}-{row["patient_name"]}-T01-{str(row["no"]).rjust(3, "0")}.xml'

            with open(file=f'{file_dir}/{row["patient_name"]}/{tmp_file_name}', encoding='utf-8', mode='w',
                      newline='') as f:
                f.writelines(row["content"])

            # 创建后台任务执行生成zip文件
            # executor = ThreadPoolExecutor(max_workers=1)
            # loop = asyncio.get_event_loop()
            # loop.run_in_executor(executor, create_examples_zip, dir_name=dir_path, is_service=False)

        cursor.close()
        cda.conn.commit()
        assert is_have_cda, "未查询到CDA"
        # 创建后台任务执行生成zip文件
        info.context['background_tasks'].add_task(create_examples_zip, dir_name=dir_path, is_service=False)

        return f'{info.context.get('request').base_url}static/temp/archive-cdas-{dir_path}.zip'


schema = strawberry.federation.Schema(query=Query)
router = GraphQLRouter(schema=schema)


if __name__ == "__main__":
    pass
