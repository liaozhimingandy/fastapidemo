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
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}/")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/api/chat/")
async def chat():
    return "Hello World"
if __name__ == "__main__":
    pass
