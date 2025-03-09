#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: FastAPIDemo
    @File： utils.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/17 11:01
    @Desc: 
=================================================
"""
import warnings

# 启用 DeprecationWarning 显示
warnings.simplefilter("always", DeprecationWarning)

def deprecated(func):
    """
    定义装饰器来标记方法为过时

    Args:
        func: 被装饰的函数

    Returns:
        wrapper: 装饰后的函数
    """
    def wrapper(*args, **kwargs):
        warnings.warn(f"'{func}' is deprecated and will be removed in the future.", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper


def main(*args, **kwargs) -> None:
    pass


if __name__ == "__main__":
    main()
