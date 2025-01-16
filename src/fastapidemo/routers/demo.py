#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: FastAPIDemo
    @File： demo.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/4 09:56
    @Desc: 
================================================="""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapidemo.model.cda import Test
from fastapidemo.model.database import get_session

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}/")
async def say_hello(name: str, session: AsyncSession = Depends(get_session)):
    statement = select(Test).where(Test.name == name)
    result = await session.execute(statement)
    test = result.scalar().first()

    return {"message": f"Hello {test.name}"}


@router.get("/api/chat/")
async def chat():
    return "Hello World"


if __name__ == "__main__":
    pass
