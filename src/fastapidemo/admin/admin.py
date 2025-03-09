#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: FastAPIDemo
    @File： admin.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/16 16:53
    @Desc: 后台管理模块
=================================================
"""
import inspect
from typing import Type, Optional, List, Any, Dict

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..model.database import get_session
from ..utils import deprecated

# 注册后台管理类
admin_registry = {}

# 创建一个 FastAPI 路由，用于展示管理界面


def get_names_admin_registry():
    """
    获取已注册的模型名称列表

    Returns:
        模型名称字典
    """
    mapping = {}
    for model, admin_class in admin_registry.items():
        mapping[model.__name__.lower()] = model
    return mapping

def register(model: Type):
    """装饰器：将管理类注册到 admin_registry"""

    def decorator(admin_class):
        admin_class._is_registered = True
        admin_class._model_class = model
        admin_registry[model] = admin_class
        return admin_class
    return decorator

@deprecated
async def register_admin(app: FastAPI):
    """注册后台管理路由"""
    # 导入admin
    from src.fastapidemo.model import admin

    # 遍历注册路由
    for model, admin_class in admin_registry.items():
        model_name = model.__name__.lower()


        # 生成列表视图的路由
        @app.get(f"/admin/{model_name}s/", summary="获取对象列表", tags=["admin"])
        async def list_view(session: AsyncSession = Depends(get_session)) -> List[model]:
            """ 展示所有 """
            ad = admin_class(model)
            items = await ad.get_queryset(session)
            return {"items": f"{items}"}

        # 详情视图
        @app.get(f"/admin/{model_name}s/{{item_id}}/detail/", summary="获取单个对象", tags=["admin"])  # , response_class=HTMLResponse
        async def detail_view(item_id: int, session: AsyncSession = Depends(get_session)) -> model:
            admin = admin_class(model)
            item = await admin.get_object(session, item_id)
            if not item:
                raise HTTPException(status_code=404, detail=f"{model_name.capitalize()} not found")
            # return templates.TemplateResponse(f"admin/{model_name}_detail.html", {"request": request, "item": item})
            return {"item": item}

def discover_and_register_admin(module: str):
    """
    自动发现并注册指定模块中使用了 `admin.register` 装饰器的管理类
    :param app: FastAPI 实例
    :param module: 包或模块的名称，字符串类型
    """
    # 加载模块
    import importlib
    module_obj = importlib.import_module(f"src.fastapidemo.model.{module}")

    # 查找模块中所有的类，并且检查是否使用了 `@register` 装饰器
    for name, obj in inspect.getmembers(module_obj):
        if inspect.isclass(obj) and hasattr(obj, "_is_registered"):  # 如果类已被注册
            # 自动注册类
            model = obj._model_class  # 获取模型类
            if model:
                register(model)(obj)  # 注册类


class ModelAdmin:
    """
    ModelAdmin 基类，包含一些通用的管理功能
    """

    model: Type  # 绑定模型类
    list_display: Optional[list] = None  # 需要展示的字段列表

    def __init__(self, model: Type):
        self.model = model
        self.list_display = self.list_display or [column.name for column in model.__table__.columns]

    async def get_queryset(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Any] | None:
        """
        获取模型的查询集

        Args:
            session: 数据库会话对象
            skip: 跳过第几行
            limit: 限制返回多少条数据

        Returns:
            1. 列表数据
            2. 或者空
        """
        statement = select(self.model).offset(skip).limit(limit)
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_object(self, session: AsyncSession, obj_id: int) -> Any | None:
        """
        根据 ID 获取单个对象

        Args:
            obj_id: 模型对象主键ID

        Returns:
            返回对象或者空数据集

        """
        statement = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(statement)
        return result.scalars().first()

    def get_fields(self):
        """ 返回模型的字段 """
        return [column.name for column in self.model.__table__.columns]





