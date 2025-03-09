from sqlmodel import SQLModel, Field

class DJANGO_MIGRATIONS(SQLModel, table=True):
    id: int = Field(None, description='', sa_column_kwargs={'comment': ''})
    app: str = Field(None, max_length=255, description='', sa_column_kwargs={'comment': ''})
    name: str = Field(None, max_length=255, description='', sa_column_kwargs={'comment': ''})
    applied: datetime = Field(None, description='', sa_column_kwargs={'comment': ''})


class CHAT_COMMENT(SQLModel, table=True):
    id: int = Field(None, description='', sa_column_kwargs={'comment': ''})
    comment_id: str = Field(None, description='评论ID', sa_column_kwargs={'comment': '评论ID'})
    is_root: bool = Field(None, description='是否为一级评论', sa_column_kwargs={'comment': '是否为一级评论'})
    parent_id: str | None = Field(None, description='父评论', sa_column_kwargs={'comment': '父评论'})
    content: str = Field(None, description='评论内容', sa_column_kwargs={'comment': '评论内容'})
    account_id: str = Field(None, max_length=7, description='评论者', sa_column_kwargs={'comment': '评论者'})
    post_id: str = Field(None, description='内容', sa_column_kwargs={'comment': '内容'})
    gmt_created: datetime = Field(None, description='创建日期时间', sa_column_kwargs={'comment': '创建日期时间'})


class CHAT_IMAGE(SQLModel, table=True):
    id: int = Field(None, description='', sa_column_kwargs={'comment': ''})
    image_name: str | None = Field(None, max_length=128, description='图片名称', sa_column_kwargs={'comment': '图片名称'})
    image_md5: str | None = Field(None, description='图片md值', sa_column_kwargs={'comment': '图片md值'})
    gmt_created: datetime = Field(None, description='', sa_column_kwargs={'comment': ''})


class CHAT_POST(SQLModel, table=True):
    id: int = Field(None, description='', sa_column_kwargs={'comment': ''})
    post_id: str = Field(None, description='帖子ID', sa_column_kwargs={'comment': '帖子ID'})
    content: str = Field(None, description='内容', sa_column_kwargs={'comment': '内容'})
    account_id: str | None = Field(None, max_length=7, description='用户ID', sa_column_kwargs={'comment': '用户ID'})
    from_ip: str = Field(None, description='来源ip', sa_column_kwargs={'comment': '来源ip'})
    from_device: int = Field(None, description='来源设备名称', sa_column_kwargs={'comment': '来源设备名称'})
    right_status: int = Field(None, description='权限状态', sa_column_kwargs={'comment': '权限状态'})
    location: str | None = Field(None, max_length=64, description='位置', sa_column_kwargs={'comment': '位置'})
    is_top: bool = Field(None, description='是否置顶', sa_column_kwargs={'comment': '是否置顶'})
    content_class: int = Field(None, description='内容类型', sa_column_kwargs={'comment': '内容类型'})
    latitude: str | None = Field(None, description='经度', sa_column_kwargs={'comment': '经度'})
    longitude: str | None = Field(None, description='纬度', sa_column_kwargs={'comment': '纬度'})
    status: int = Field(None, description='帖子状态', sa_column_kwargs={'comment': '帖子状态'})
    gmt_created: datetime = Field(None, description='创建日期时间', sa_column_kwargs={'comment': '创建日期时间'})


class CHAT_LIKE(SQLModel, table=True):
    id: int = Field(None, description='', sa_column_kwargs={'comment': ''})
    post_id: str = Field(None, description='帖子ID', sa_column_kwargs={'comment': '帖子ID'})
    account_id: str | None = Field(None, max_length=7, description='点赞的用户', sa_column_kwargs={'comment': '点赞的用户'})
    gmt_created: datetime = Field(None, description='创建日期时间', sa_column_kwargs={'comment': '创建日期时间'})


class CHAT_ACCOUNT(SQLModel, table=True):
    id: int = Field(None, description='', sa_column_kwargs={'comment': ''})
    account_id: str = Field(None, max_length=7, description='用户ID', sa_column_kwargs={'comment': '用户ID'})
    username: str = Field(None, max_length=7, description='用户名', sa_column_kwargs={'comment': '用户名'})
    nick_name: str = Field(None, max_length=64, description='昵称', sa_column_kwargs={'comment': '昵称'})
    email: str | None = Field(None, max_length=254, description='电子邮箱', sa_column_kwargs={'comment': '电子邮箱'})
    gmt_birth: datetime.datetime | None = Field(None, description='出生日期', sa_column_kwargs={'comment': '出生日期'})
    areaCode: str | None = Field(None, max_length=3, description='区域代码', sa_column_kwargs={'comment': '区域代码'})
    mobile: str | None = Field(None, max_length=32, description='电话号码', sa_column_kwargs={'comment': '电话号码'})
    sex: int = Field(None, description='性别', sa_column_kwargs={'comment': '性别'})
    avatar: str = Field(None, max_length=200, description='头像链接', sa_column_kwargs={'comment': '头像链接'})
    is_active: bool = Field(None, description='账户状态', sa_column_kwargs={'comment': '账户状态'})
    user_type: int = Field(None, description='账户状态', sa_column_kwargs={'comment': '账户状态'})
    password: str | None = Field(None, max_length=128, description='用户密码', sa_column_kwargs={'comment': '用户密码'})
    allow_add_friend: bool = Field(None, description='允许添加好友', sa_column_kwargs={'comment': '允许添加好友'})
    allow_beep: bool = Field(None, description='是否允许提示音', sa_column_kwargs={'comment': '是否允许提示音'})
    allow_vibration: bool = Field(None, description='是否允许震动提示', sa_column_kwargs={'comment': '是否允许震动提示'})
    gmt_created: datetime = Field(None, description='创建日期时间', sa_column_kwargs={'comment': '创建日期时间'})
    im_id: str | None = Field(None, max_length=64, description='im ID', sa_column_kwargs={'comment': 'im ID'})
    salt: str = Field(None, max_length=8, description='盐', sa_column_kwargs={'comment': '盐'})
    gmt_modified: datetime = Field(None, description='最后修改时间', sa_column_kwargs={'comment': '最后修改时间'})


class CHAT_APP(SQLModel, table=True):
    id: int = Field(None, description='', sa_column_kwargs={'comment': ''})
    app_id: str = Field(None, max_length=7, description='appid', sa_column_kwargs={'comment': 'appid'})
    app_secret: str = Field(None, max_length=32, description='应用密钥', sa_column_kwargs={'comment': '应用密钥'})
    salt: str = Field(None, max_length=8, description='盐', sa_column_kwargs={'comment': '盐'})
    app_name: str = Field(None, max_length=32, description='应用名称', sa_column_kwargs={'comment': '应用名称'})
    app_en_name: str | None = Field(None, max_length=64, description='应用英文名称', sa_column_kwargs={'comment': '应用英文名称'})
    is_active: bool = Field(None, description='激活状态', sa_column_kwargs={'comment': '激活状态'})
    gmt_created: datetime = Field(None, description='创建日期时间', sa_column_kwargs={'comment': '创建日期时间'})
    gmt_updated: datetime = Field(None, description='最后更新日期时间', sa_column_kwargs={'comment': '最后更新日期时间'})


