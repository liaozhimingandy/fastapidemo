#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: FastAPIDemo
    @File： admin.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/16 16:58
    @Desc: 
=================================================
"""

from src.fastapidemo.admin import admin
from src.fastapidemo.model.cda import Test, C0017


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age']


@admin.register(C0017)
class C0017Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age']


if __name__ == "__main__":
    pass
