from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from fastapidemo import hiptools_router, demo_router

# 加载环境变量
_ = load_dotenv(find_dotenv())

# 配置允许跨域的域名、请求方法等
origins = [
    "http://localhost",  # 允许本地开发环境的前端应用访问
    "http://localhost:5173",  # 如果你使用的是 React 或 Vue 的开发服务器
    "http://api.esb.alsoapp.com",
]

app = FastAPI()

# 启用 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的域名列表
    allow_credentials=True,  # 允许携带 cookie
    allow_methods=["GET", "POST", "OPTIONS", "PUT"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的请求头
)

app.include_router(demo_router)
app.include_router(hiptools_router, prefix="/graphql")
# 获取项目根目录
base_dir = Path(__file__).resolve().parent
# 设置静态文件目录
static_dir = base_dir / "static"
# 挂载静态文件目录到 /static 路径
app.mount("/static", StaticFiles(directory=static_dir), name="static")
