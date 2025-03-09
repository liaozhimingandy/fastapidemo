#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: FastAPIDemo
    @File： __init__.py.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/19 09:19
    @Desc: 
=================================================
"""
from src.fastapidemo.account.views import router as account_router
from src.fastapidemo.account.models import ACCOUNT, APP
