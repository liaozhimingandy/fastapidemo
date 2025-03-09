#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=================================================
    @Project: FastAPIDemo
    @File： views.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/19 09:45
    @Desc: 
=================================================
"""
import os
import uuid

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import APP
from src.fastapidemo.model.database import get_session

# from src.fastapidemo.account.token import generate_jwt_token

router = APIRouter(tags=["account"])

@router.get("/authorize/{app_id}/{app_secret}/client_credential/", summary="用户进行认证获取刷新令牌")
async def authorize(app_id: str, app_secret: str, session: AsyncSession = Depends(get_session)):
    """
    用户进行认证获取刷新令牌

    Args:
        app_id: 应用唯一标识 <br>
        app_secret: 应用密钥 <br>

    Returns:
        令牌信息或报错信息

    """

    try:
        assert len(app_secret) > 0, "app_secret must exists"
        # app = App.objects.get(app_id=app_id.replace(os.getenv(('PREFIX_ID'), ''), app_secret=app_secret, is_active=True)
        statement = select(APP).where(APP.app_id == app_id.replace(os.getenv('PREFIX_ID', ''), ''),
                                                                               APP.app_secret == app_secret,
                                                                               APP.is_active == "1")
        print(statement)
        reuslts = await session.execute(statement)
        app = reuslts.scalar().first()
        print(app)
    except AssertionError as e:
        return 403, {"message": str(e)}


    # 作废之前的salt
    # app.salt = uuid.uuid4().hex[:8]
    # app.save()
    # data = {"app_id": app_id, "salt": app.salt}

    # token_refresh = generate_jwt_token(data, expires_in=timedelta(days=7), grant_type=grant_type)
    # token_access = generate_jwt_token(data, grant_type="access_token")
    # token_refresh.update(**{"app_id": app_id, "refresh_token": token_refresh.get("access_token", None)})
    # return 200, token_refresh
    return {"message": "success"}


@router.get("/refresh-token/{app_id}/refresh_token/", summary="使用刷新令牌进行更新获取权限令牌")
def refresh_token(app_id: str):
    """

     使用刷新令牌进行更新获取权限令牌,请使用postman测试,header携带认证信息,后续会实现,refresh_token有效期为7天,请妥善保管,重新登录认证后,
     该token作废;

    :param request: 请求对象<br>
    :param authorization: Bearer 您的refresh_token <br>
    :param app_id: 应用唯一标识 <br>
    :return:
    """
    # authorization = request.META.get('HTTP_AUTHORIZATION', '').split()[1] # 从请求头获取token
    # 使用JWT认证模块进行认证,借用user对象存储相关信息

    # try:
    #     app = App.objects.get(app_id=app_id.replace(settings.PREFIX_ID, ''), is_active=True)
    #     assert request.user.username == app.salt, "app_secret or salt changed, please login again!"
    # except App.DoesNotExist:
    #     return 403, {"message": "Not Found"}
    # except AssertionError as e:
    #     return 403, {"message": str(e)}
    #
    # data = {"app_id": app_id, "salt": app.salt, "jwt_app_id": app_id}
    #
    # # 生成请求令牌
    # token_access = generate_jwt_token(data, grant_type="access_token")
    # token_access.update(**{"app_id": app_id})

    return {"message": "success"}


@router.get("test-oauth/", summary="测试接口")
def test_oauth():
    return 200, {"message": "hello word"}
