#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: FastAPIDemo
    @File： test_main.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/5 21:25
    @Desc: 
================================================="""
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_main():
    response = client.get("/")
    assert response.status_code == 200

def test_say_hello():
    response = client.get("/hello/zhiming/")
    assert response.status_code == 200
    assert response.text == "Hello, zhiming"


if __name__ == "__main__":
    pass
