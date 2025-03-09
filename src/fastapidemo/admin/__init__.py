#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: FastAPIDemo
    @File： __init__.py.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/16 16:57
    @Desc: 
=================================================
"""

from .admin import discover_and_register_admin
from .views import router as admin_router