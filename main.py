from pathlib import Path
from contextlib import asynccontextmanager

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.fastapidemo.demo import demo_router
from src.fastapidemo.hiptools import hiptools_router
from src.fastapidemo.account import account_router
from src.fastapidemo.admin import admin_router, discover_and_register_admin

# 加载环境变量
_ = load_dotenv(find_dotenv(filename=".env.dev"))

# 配置允许跨域的域名、请求方法等
origins = [
    "http://localhost",  # 允许本地开发环境的前端应用访问
    "http://localhost:5173",  # 如果你使用的是 React 或 Vue 的开发服务器
    "https://www.alsoapp.com" # 允许线上环境的前端应用访问
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动时执行的操作"""
    # 在这里执行你需要在应用启动时执行的操作，比如初始化数据库连接等
    # 例如：
    # await init_db()

    # 初始化管理路由
    # await admin.register_admin(app)
    discover_and_register_admin("admin")
    yield
    # 在这里执行你需要在应用关闭时执行的操作，比如关闭数据库连接等
    # 例如：
    # await close_db()

app = FastAPI()

# 启用 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的域名列表
    allow_credentials=True,  # 允许携带 cookie
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的请求头
)

app.include_router(demo_router)
app.include_router(hiptools_router, prefix="/graphql", tags=["graphql"])
# 注册后台管理路由
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(account_router)

# 获取项目根目录
base_dir = Path(__file__).resolve().parent
# 设置静态文件目录
static_dir = base_dir / "static"
# 挂载静态文件目录到 /static 路径
app.mount("/static", StaticFiles(directory=static_dir), name="static")

