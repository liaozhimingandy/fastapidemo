#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: FastAPIDemo
    @File： views.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/19 08:44
    @Desc: 
=================================================
"""
from typing import Dict, List, Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .admin import admin_registry, get_names_admin_registry
from ..model.database import get_session

router = APIRouter()


@router.get("/models/", response_model=list[str], summary="获取已注册的模型列表", tags=["admin"])
def get_registered_models():
    """返回已注册的模型列表"""
    return get_names_admin_registry().keys()

@router.get("/{model_name}/", summary="根据模型名称,获取该模型对象列表数据", tags=["admin"])
async def get_model_data(model_name: str, skip: int = 0, limit: int = 10,
                         session: AsyncSession = Depends(get_session),
                         model_class_names = Depends(get_names_admin_registry)) -> Dict[str,List[Any]] | None:

    """
    根据模型名称,获取该模型对象列表数据

    Args:
        model_name: 模型名称
        skip: 跳过第几行
        limit: 限制返回多少条数据
        session: 数据库会话对象
        model_class_names: 模型名称到模型类的映射字典

    Returns:
        返回对象或者空数据集
    """

    # 通过模型名称获取模型类
    model_class = model_class_names.get(model_name.lower())

    if model_class is None:
        raise HTTPException(status_code=404, detail="Model Not Found")

    # 从admin_registry获取对应的模型和管理类
    model_admin_class = admin_registry.get(model_class)
    model_admin = model_admin_class(model_class)

    # 异步查询数据
    items = await model_admin.get_queryset(session, skip=skip, limit=limit)

    return {"items": items}

@router.get("/{model_name}/detail/{item_id}", summary="根据模型名称,获取该模型对象详情数据", tags=["admin"])
async def get_model_detail_data(model_name: str, item_id: int,
                                 session: AsyncSession = Depends(get_session),
                                 model_class_names = Depends(get_names_admin_registry)) -> Dict[str,Any] | None:
    """
    根据模型名称,获取该模型对象详情数据

    Args:
        model_name: 模型名称
        item_id: 模型对象主键ID
        session: 数据库会话对象
        model_class_names: 模型名称到模型类的映射字典

    Returns:
        返回对象或者空数据集
    """

    # 通过模型名称获取模型类
    model_class = model_class_names.get(model_name.lower())
    if model_class is None:
        raise HTTPException(status_code=404, detail="Model Not Found")

    # 从admin_registry获取对应的模型和管理类
    model_admin_class = admin_registry.get(model_class)
    model_admin = model_admin_class(model_class)

    # 异步查询数据
    item = await model_admin.get_object(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item Not Found")

    return {"item": item}

