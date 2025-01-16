#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: FastAPIDemo
    @File： database.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2025/1/11 11:44
    @Desc: 
================================================="""
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, select

# 创建异步引擎
sqlite_file_name = "database.sqlite3"
DATABASE_URL = f"sqlite+aiosqlite:///{sqlite_file_name}"
# DATABASE_URL = "postgresql+psycopg://zhiming:zhiming@localhost:5432/cda"
engine = create_async_engine(DATABASE_URL, echo=False)  # Annotated[bool, Doc("是否显示数据库层面日志")]

# 创建异步session
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


def create_db_and_table():
    """创建所有数据库和表"""
    SQLModel.metadata.create_all(engine)
    # 删除所有表
    # SQLModel.metadata.drop_all(engine)


# 获取异步session的依赖
async def get_session() -> AsyncSession:
    """获取数据库会话"""
    async with AsyncSessionLocal() as session:
        yield session


async def create_db_async():
    """创建数据库"""
    from cda import Test, C0017, C0018
    async with engine.begin() as conn:
        # 使用 SQLAlchemy 的异步连接创建表
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Tables created successfully")  # 添加日志输出，确认创建


async def example() -> None:
    from cda import Test

    # 获取数据库session
    async for session in get_session():
        async with session.begin():
            data = {"name": "zhiming", "age": 10, "gender_code": 1}
            try:
                test = Test(**data)
                test_valid = test.model_validate(test)
                print(test_valid)
                session.add(test)
                await session.flush()  # 刷新session，将数据提交到数据库，但不提交事务
                await session.refresh(test)
                await session.commit()  # 提交事务
                print(test)
            except Exception as e:
                print(f"错误信息: {str(e)}")
                await session.rollback()  # 回滚事务
            print(session.is_active)
        #   查询数据
        statement = select(Test).where(Test.name == "zhiming")
        result = await session.execute(statement)
        test = result.scalars().first()
        print(test)


async def main():
    # await example()
    # 创建表
    await create_db_async()


if __name__ == "__main__":
    asyncio.run(main())
