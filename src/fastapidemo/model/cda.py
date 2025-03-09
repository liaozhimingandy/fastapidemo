#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: FastAPIDemo
    @File： cda.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/10 16:54
    @Desc: 第三代电子病历共享文档(CDA)模型
=================================================
"""
from enum import Enum
from decimal import Decimal
from datetime import datetime, date

from sqlalchemy import Boolean, SMALLINT
from sqlmodel import SQLModel, Field

TABLE_PREFIX = "cda"


class GenderEnum(Enum):
    """
    性别枚举
    """
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


class BaseModel(SQLModel, table=False):
    """
    CAD模型公共信息部分
    """

    id: int | None = Field(default=None, primary_key=True, description="表主键", title="表主键",
                           sa_column_kwargs={"comment": "表主键"})
    gmt_created: datetime = Field(default_factory=datetime.now, description="记录创建日期时间",
                                  sa_column_kwargs={"comment": "记录创建日期时间"})
    is_finished: bool = Field(default=False, sa_type=Boolean, description="文档完成标识,1:已完成生成,0未生成,默认为0",
                              sa_column_kwargs={"comment": "完成标识"})
    gmt_finish: datetime | None = Field(None, description="文档生成日期时间",
                                        sa_column_kwargs={"comment": "文档生成日期时间"})
    doc_id: str = Field(..., max_length=36, description="文档流水号",
                         index=True, sa_column_kwargs={"comment": "文档流水号"})
    adm_no: str = Field(..., max_length=36, description="就诊流水号", index=True,
                        sa_column_kwargs={"comment": "就诊流水号"})
    data_src: str = Field(..., max_length=36, description="数据来源,请参照主数据标准字典:医疗卫生机构",
                          sa_column_kwargs={"comment": "数据来源"})


class Position(SQLModel, table=False):
    """
    位置信息, 科室,病区,病房,病床
    """
    dept_id: str = Field(..., max_length=36, description="科室代码")
    dept_name: str = Field(..., max_length=36, description="科室名称")
    ward_code: str | None = Field(None, max_length=36, description="病区代码")
    ward_name: str | None = Field(None, max_length=36, description="病区名称")
    ward_id: str | None = Field(None, max_length=36, description="病房号id")
    ward_no: str | None = Field(None, max_length=36, description="病房号")
    bed_id: str | None = Field(None, max_length=36, description="病床号Id")
    bed_no: str | None = Field(None, max_length=36, description="病床号")


class Test(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., description="姓名")
    age: int = Field(..., description="年龄", le=150, ge=0)
    gender_code: GenderEnum = Field(default=GenderEnum.UnKnown, description="性别代码", sa_type=SMALLINT)


    @property
    def gender_name(self):
        return GenderEnum(self.gender_code).label  # 自动转换为枚举类型


class C0017(Position, BaseModel, table=True):
    """
    一般护理记录
    """

    __tablename__ = f"{TABLE_PREFIX}_c0017"  # 表名
    __table_args__ = {'comment': '一般护理记录'}  # 表备注
    
    inpatient_id: str = Field(..., max_length=18, description='住院号')
    id_no:str = Field(..., max_length=18, description='患者身份证件号码')
    name:str = Field(..., max_length=50, description='患者姓名')
    gender_code: GenderEnum = Field(default=GenderEnum.UnKnown.value, description="性别代码",
                                    sa_type=SMALLINT, le=10, ge=0)
    gender_name: str | None = Field(None, max_length=10, description="性别名称")
    age: int = Field(..., description="年龄", le=150, ge=0, sa_type=SMALLINT)
    age_unit:str = Field(..., max_length=8, description='年龄单位')
    provider_org_id:str = Field(..., max_length=18, description='医疗机构组织机构代码(提供患者服务机构)')
    provider_org_name:str = Field(..., max_length=64, description='医疗机构组织机构名称(提供患者服务机构)')
    create_date:str = Field(..., max_length=8, description='文档创作日期')
    author_id:str = Field(..., max_length=50, description='护士工号(文档创作者)')
    author_name:str = Field(..., max_length=50, description='护士签名(文档创作者)')
    gen_doc_org_id:str = Field(..., max_length=18, description='医疗机构组织机构代码(文档生成机构)')
    gen_doc_org_name:str = Field(..., max_length=64, description='医疗机构组织机构名称(文档生成机构)')
    signature_datetime:str = Field(..., max_length=15, description='签名日期时间')
    nurse_id:str = Field(..., max_length=36, description='护士工号')
    nurse_name:str = Field(..., max_length=50, description='护士签名')
    disease_diagnosis_code: str | None = Field(default=None, max_length=36, description='疾病诊断编码')
    disease_diagnosis_name: str | None = Field(..., max_length=64, description='疾病诊断编码')
    allergic_history: str | None = Field(..., description='过敏史')
    pulse_rate: int = Field(..., description='脉率(次/min)', ge=0)
    weight: Decimal = Field(None, description="体重（kg）", max_digits=5, decimal_places=1)
    temperature: Decimal = Field(None, description="体温（℃）", max_digits=4, decimal_places=1)
    heart_rate: int = Field(None, description="心率（次/min）", le=300, ge=0)
    systolic_pressure: int = Field(None, description="收缩压（mmHg）", le=200, ge=50)
    diastolic_pressure: int = Field(None, description="舒张压（mmHg）", le=100, ge=0)
    blood_oxygen_saturation: int = Field(..., max_digits=4, decimal_places=1, description='血氧饱和度(%%)')
    dorsalartery_foot_flag: bool = Field(...,  description='足背动脉搏动标志')
    diet_code:str = Field(..., max_length=1, description='饮食情况代码')
    diet_name:str = Field(..., max_length=10, description='饮食情况名称')
    dietary_guidance_code:str = Field(..., max_length=2, description='饮食指导代码')
    dietary_guidance_name:str = Field(..., max_length=10, description='饮食指导名称')
    nursing_grade_code:str = Field(..., max_length=1, description='护理等级代码')
    nursing_grade_name:str = Field(..., max_length=10, description='护理等级名称')
    nursing_type_code:str = Field(..., max_length=1, description='护理类型代码')
    nursing_type_name:str = Field(..., max_length=10, description='护理类型名称')
    catheter_care_desc: str = Field(..., max_length=255, description='导管护理描述')
    tracheal_care_code:str = Field(..., max_length=1, description='气管护理代码')
    tracheal_care_name:str = Field(..., max_length=1, description='气管护理名称')
    postural_nursing:str = Field(..., max_length=30, description='体位护理')
    skin_care_desc:str = Field(..., max_length=50, description='皮肤护理')
    nutrition_nursing:str = Field(..., max_length=100, description='营养护理')
    mental_nursing_code:str = Field(..., max_length=1, description='心理护理代码')
    mental_nursing_name:str = Field(..., max_length=50, description='心理护理名称')
    safety_nursing_code:str = Field(..., max_length=1, description='安全护理代码')
    safety_nursing_name:str = Field(..., max_length=30, description='安全护理名称')
    brief_condition: str = Field(..., description='简要病情')
    nursing_observation_item_name:str = Field(..., max_length=30, description='护理观察项目名称')
    nursing_observation_result:str = Field(..., description='护理观察结果')
    nursing_operation_name:str = Field(..., max_length=100, description='护理操作名称')
    nursing_operation_item_cls_name:str = Field(..., max_length=100, description='护理操作项目类目名称')
    nursing_operation_result: str =Field(..., description='护理操作结果')
    send_operation_safety_checklist_flag: bool = Field(default=False, description='发出手术安全核对表标志')
    rcv_operation_safety_checklist_flag: bool = Field(default=False, description='收回手术安全核对表标志')
    send_risk_assessment_flag: bool = Field(default=False, description='发出手术风险评估表标志')
    rcv_risk_assessment_flag: bool = Field(default=False, description='收回手术风险评估表标志')
    isolation_flag: bool = Field(default=False, description='隔离标志')
    isolation_cls_code:str = Field(..., max_length=8, description='隔离种类代码')
    isolation_cls_name:str = Field(..., max_length=100, description='隔离种类名称')

        
class C0018(Position, BaseModel, table=True):
    """
    病重（病危）护理记录
    """
    # 表名
    __tablename__ = f"{TABLE_PREFIX}_c0018"
    __table_args__ = {'comment': '病重（病危）护理记录'}  # 表备注

    inpatient_id: str | None = Field(None, max_length=36, description="住院号")
    id_no: str = Field(..., max_length=36, description="患者身份证件号码")
    name: str = Field(..., max_length=64, description="患者姓名")
    gender_code: GenderEnum = Field(default=GenderEnum.UnKnown.value, description="性别代码",
                                    sa_type=SMALLINT, le=10, ge=0)
    gender_name: str | None = Field(None, max_length=10, description="性别名称")
    age: int = Field(..., description="年龄", le=150, ge=0)
    age_unit: str = Field(..., max_length=2, description="年龄单位")
    provider_org_id: str = Field(..., max_length=18, min_length=18,
                                 description="医疗机构组织机构代码(提供患者服务机构)")
    provider_org_name: str = Field(..., max_length=36, description="医疗机构组织机构名称(提供患者服务机构)")
    create_date: date = Field(..., max_length=8, description="文档创作日期")
    author_id: str = Field(..., max_length=36, description="护士工号(文档创作者)")
    author_name: str = Field(..., max_length=36, description="护士签名(文档创作者)")
    gen_doc_org_id: str = Field(..., max_length=18, min_length=18, description="医疗机构组织机构代码(文档生成机构)")
    gen_doc_org_name: str = Field(..., max_length=18, description="医疗机构组织机构名称(文档生成机构)")
    gmt_signature: datetime = Field(..., description="签名日期时间")
    nurse_id: str | None = Field(None, max_length=36, description="护士工号")
    nurse_name: str | None = Field(None, max_length=36, description="护士签名")
    allergic_flag: bool = Field(default=False, description="过敏史标志")
    allergic_history: str | None = Field(None, description="过敏史")
    disease_diagnosis_code: str | None = Field(None, max_length=36, description="疾病诊断编码")
    disease_diagnosis_name: str | None = Field(None, max_length=64, description="疾病诊断名称")
    weight: Decimal = Field(None, description="体重（kg）", max_digits=5, decimal_places=1)
    temperature: Decimal = Field(None, description="体温（℃）", max_digits=4, decimal_places=1)
    heart_rate: int = Field(None, description="心率（次/min）", le=300, ge=0)
    respiratory_rate: int = Field(None, description="呼吸频率（次/min）", le=100, ge=0)
    systolic_pressure: int = Field(None, description="收缩压（mmHg）", le=200, ge=50)
    diastolic_pressure: int = Field(None, description="舒张压（mmHg）", le=100, ge=0)
    blood_sugar_value: Decimal = Field(None, description="血糖检测值（mmol/L）", max_digits=3, decimal_places=1)
    diet_code: str = Field(None, max_length=1, description="饮食情况代码")
    diet_name: str | None = Field(None, max_length=10, description="饮食情况名称")
    nursing_grade_code: str = Field(None, max_length=1, description="护理等级代码")
    nursing_grade_name: str | None = Field(None, max_length=10, description="护理等级名称")
    nursing_type_code: str | None = Field(None, max_length=1, description="护理类型代码")
    nursing_type_name: str | None = Field(None, max_length=10, description="护理类型名称")
    nursing_observation_item_name: str | None = Field(None, max_length=30, description="护理观察项目名称")
    nursing_observation_result: str | None = Field(None, description="护理观察结果")
    nursing_operation_name: str | None = Field(None, max_length=100, description="护理操作名称")
    nursing_operation_item_cls_name: str | None = Field(None, max_length=100, description="护理操作项目类目名称")
    nursing_operation_result: str | None = Field(None, description="护理操作结果")
    ventilator_monitoring_item: str | None = Field(None, max_length=64, description="呼吸机监护项目")

    # 不添加数据库层面约束, 由业务层面约束
    # __table_args__ = (
    #     CheckConstraint('age > 0 AND age < 150', name='check_age_range'),   # SQLAlchemy层面的约束
    #     CheckConstraint(f'gender_code IN {tuple([e.value[0] for e in GenderEnum])}', name='check_gender_code_value'),
    #     CheckConstraint('diastolic_pressure < systolic_pressure', name='check_diastolic_pressure_less_than_systolic_pressure'),
    # )

        
class C0020(Position, BaseModel, table=True):
    """
    生命体征测量记录
    """
    # 表名
    __tablename__ = f"{TABLE_PREFIX}_c0020"
    __table_args__ = {'comment': '生命体征测量记录'}  # 表备注

    doc_id: str = Field(None, max_length=32, description='文档流水号', sa_column_kwargs={'comment': '文档流水号'})
    inpatientId: str = Field(None, max_length=18, description='住院号', sa_column_kwargs={'comment': '住院号'})
    id_no: str = Field(None, max_length=18, description='患者身份证件号码', sa_column_kwargs={'comment': '患者身份证件号码'})
    name: str = Field(None, max_length=50, description='患者姓名', sa_column_kwargs={'comment': '患者姓名'})
    gender_code: GenderEnum = Field(default=GenderEnum.UnKnown.value, description="性别代码", sa_type=SMALLINT, le=10, ge=0)
    gender_name: str | None = Field(None, max_length=10, description="性别名称")
    age: int = Field(..., description='年龄', sa_column_kwargs={'comment': '年龄'})
    age_unit: str = Field(default="岁", max_length=4, description='年龄单位', sa_column_kwargs={'comment': '年龄单位'})
    provider_org_id: str = Field(..., max_length=18, description='医疗机构组织机构代码(提供患者服务机构)', sa_column_kwargs={'comment': '医疗机构组织机构代码(提供患者服务机构)'})
    provider_org_name: str = Field(..., max_length=64, description='医疗机构组织机构名称(提供患者服务机构)', sa_column_kwargs={'comment': '医疗机构组织机构名称(提供患者服务机构)'})
    create_date: date = Field(..., max_length=8, description='文档创作日期', sa_column_kwargs={'comment': '文档创作日期'})
    author_id: str = Field(..., max_length=36, description='护士工号(文档创作者)', sa_column_kwargs={'comment': '护士工号(文档创作者)'})
    author_name: str = Field(..., max_length=64, description='护士签名(文档创作者)', sa_column_kwargs={'comment': '护士签名(文档创作者)'})
    gen_doc_org_id: str = Field(..., max_length=20, description='医疗机构组织机构代码(文档生成机构)', sa_column_kwargs={'comment': '医疗机构组织机构代码(文档生成机构)'})
    gen_doc_org_name: str = Field(..., max_length=10, description='医疗机构组织机构名称(文档生成机构)', sa_column_kwargs={'comment': '医疗机构组织机构名称(文档生成机构)'})
    gmt_signature: datetime = Field(..., description='签名日期时间', sa_column_kwargs={'comment': '签名日期时间'})
    nurse_id: str = Field(..., max_length=36, description='护士工号', sa_column_kwargs={'comment': '护士工号'})
    nurse_name: str = Field(..., max_length=64, description='护士签名', sa_column_kwargs={'comment': '护士签名'})
    days_after_delivery: int = Field(default=0, description='手术或分娩后天数', sa_column_kwargs={'comment': '手术或分娩后天数'}, ge=0)
    gmt_admission: datetime = Field(..., description='入院日期时间', sa_column_kwargs={'comment': '入院日期时间'})
    offset_days: int = Field(..., description='实际住院天数', sa_column_kwargs={'comment': '实际住院天数'}, ge=0)
    disease_diagnosis_code: str = Field(..., max_length=36, description='疾病诊断编码', sa_column_kwargs={'comment': '疾病诊断编码'})
    disease_diagnosis_name: str = Field(..., max_length=64, description='疾病诊断名称', sa_column_kwargs={'comment': '疾病诊断名称'})
    respiratory_rate: int = Field(None, description="呼吸频率（次/min）", le=100, ge=0, sa_column_kwargs={'comment': '呼吸频率（次/min）'})
    ventilator_use_flag: bool = Field(default=False, description='使用呼吸机标志', sa_column_kwargs={'comment': '使用呼吸机标志'})
    pulse_rate: int = Field(None, description='脉率（次/min）', sa_column_kwargs={'comment': '脉率（次/min）'}, le=300, ge=0)
    pacemaker_heart_rate: int = Field(None, description='起搏器心率（次/min）', sa_column_kwargs={'comment': '起搏器心率（次/min）'}, le=300, ge=0)
    temperature: Decimal = Field(None, description="体温（℃）", max_digits=4, decimal_places=1, sa_column_kwargs={'comment': '体温（℃）'})
    systolic_pressure: int = Field(None, description="收缩压（mmHg）", le=200, ge=50, sa_column_kwargs={'comment': '收缩压（mmHg）'})
    diastolic_pressure: int = Field(None, description="舒张压（mmHg）", le=100, ge=0, sa_column_kwargs={'comment': '舒张压（mmHg）'})
    weight: Decimal = Field(None, description="体重（kg）", max_digits=5, decimal_places=1, sa_column_kwargs={'comment': '体重（kg）'})
    abdominal_girth: Decimal = Field(..., description='腹围（cm）', max_digits=4, decimal_places=1, sa_column_kwargs={'comment': '腹围（cm）'})
    nursing_observation_item_name: str = Field(..., max_length=64, description='护理观察项目名称', sa_column_kwargs={'comment': '护理观察项目名称'})
    nursing_observation_result: str = Field(..., max_length=128, description='护理观察结果', sa_column_kwargs={'comment': '护理观察结果'})


if __name__ == "__main__":
    pass
