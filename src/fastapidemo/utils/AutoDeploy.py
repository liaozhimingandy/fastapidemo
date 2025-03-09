#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
import asyncio
import sys
from pprint import pprint

import paramiko
from fabric import Connection


def deploy(to_ip: str, from_dir: str = r'E:\ANDY\docker', to_dir: str = "/home/docker",
           docker_info: str = "docker-24.0.7.tgz", username: str = "root", password: str = "ndfskqyy@2022") -> None:
    """
    将本地目录下的文件上传到指定ip指定目录下，并自动执行install.sh脚本

    Args:
        to_ip: 待上传的服务器ip
        from_dir: 本地目录，使用绝对路径
        to_dir: 需要上传到服务器ip的路径
        docker_info: docker版本信息,如果您使用了最新的docker版本,请更新此参数
        username: 远程服务器用户名
        password: 远程服务器用户名对应的密码

    Returns:
        None
    """
    try:
        conn = Connection(to_ip, user=username, connect_kwargs={"password": password})
        conn.run('who i am')
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        print(e.args[1])
        return
    except Exception as e:
        pprint(e)
        return

    # 判断是否已经安装docker
    result = conn.run("docker --version", warn=True, hide=True)
    if not result.failed:
        pprint(f"server: {to_ip} docker is already installed!")
        return

    # 上传本地目录下所有文件到目标服务器
    pprint(f"upload file to server...{to_ip}")
    for root, dirs, files in os.walk(from_dir):
        for file in files:
            local_file_path = os.path.join(root, file)
            remote_file_path = os.path.join(to_dir, os.path.relpath(local_file_path, from_dir)).replace("\\", "/")

            # 如果没有则创建
            remote_file_dir = os.path.dirname(remote_file_path)
            conn.run(f"mkdir -p {remote_file_dir}")

            # 上传文件
            conn.put(local_file_path, remote_file_path)
            pprint(f"upload {local_file_path} success!")

    # 执行目标服务器上的脚本
    pprint("executing install.sh script...")
    conn.run(
        f"cd {to_dir} && export LANG=c.UTF-8 && chmod +x install.sh && sh {to_dir}/install.sh {to_dir}/{docker_info}")

    # 运行完后删除远程目录及下所有文件
    conn.run(f"rm -rf {to_dir}")
    pprint("congratulations, docker installation complete！")


def get_docker_images(conn: Connection) -> set:
    """
    获取镜像列表

    Args:
        conn: 连接对象

    Returns:
        镜像集合
    """
    # 获取加载后的镜像名称和标签
    result = conn.run("docker images --format '{{.Repository}}:{{.Tag}}'", hide=True)
    # 提取出所有镜像名称和标签
    return set(result.stdout.strip().split('\n'))



def upload_image(to_ip: str, from_dir: str = r'E:\ANDY\docker', to_dir: str = "/home/docker",
                 username: str = "root", password: str = "ndfskqyy@2022", registries: str="localhost:5000") -> None:
    """
    将本地目录下的文件上传到指定ip指定目录下，并且导入到镜像仓库

    Args:
        to_ip: 待上传的服务器ip
        from_dir: 本地目录，使用绝对路径
        to_dir: 需要上传到服务器ip的路径
        username: 远程服务器用户名
        password: 远程服务器用户名对应的密码
        registries: 镜像仓库地址

    Returns:
        None
    """
    try:
        conn = Connection(to_ip, user=username, connect_kwargs={"password": password})
        conn.run('who i am')
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        print(e.args[1])
        return
    except Exception as e:
        pprint(e)
        return

    # 判断是否已经安装docker
    result = conn.run("docker --version", warn=True, hide=True)
    if result.failed:
        pprint(f"server: {to_ip} docker is not installed!")
        return

    # 检查本地目录是否存在
    if not os.path.exists(from_dir):
        raise FileNotFoundError(f"本地镜像目录 {from_dir} 不存在")

    # 获取所有的 .tar 文件
    tar_files = [f for f in os.listdir(from_dir) if f.endswith('.tar')]

    if not tar_files:
        raise FileNotFoundError(f"目录 {from_dir} 中没有找到任何 Docker 镜像文件")

    # 上传本地目录下所有文件到目标服务器
    pprint(f"upload file to server...{to_ip}")
    for root, dirs, files in os.walk(from_dir):
        for file in files:
            local_file_path = os.path.join(root, file)
            remote_file_path = os.path.join(to_dir, os.path.relpath(local_file_path, from_dir)).replace("\\", "/")

            # 如果没有则创建
            remote_file_dir = os.path.dirname(remote_file_path)
            conn.run(f"mkdir -p {remote_file_dir}")

            # 上传文件
            conn.put(local_file_path, remote_file_path)
            pprint(f"upload {local_file_path} success!")

            # 导入镜像前的镜像列表
            pre_import_images = get_docker_images()

            # 导入镜像到docker引擎
            conn.run(f"docker load -i {file}")

            # 导入镜像后的镜像列表
            post_import_images = get_docker_images()

            # 获取新增的镜像
            new_images = post_import_images - pre_import_images

            # 为镜像打标签并推送到仓库
            print(f"推送镜像 {new_images} 到仓库...")
            conn.run(f"docker tag {new_images} {registries}/{new_images}")
            conn.run(f"docker push {registries}/{new_images}")

            # 移除标签
            conn.run(f"docker rmi {registries}/{new_images}")

    # 运行完后删除远程目录及下所有文件
    conn.run(f"rm -rf {to_dir}")
    pprint("congratulations, docker upload complete！")

def pull_image(to_ip: str, username: str = "root", password: str = "ndfskqyy@2022",
               registries: str="172.16.33.148:5000", image_name: str = "rhapsody:latest") -> None:
    """
    从镜像仓库下载镜像到本地

    Args:
        to_ip: 待上传的服务器ip
        username: 远程服务器用户名
        password: 远程服务器用户名对应的密码
        registries: 镜像仓库地址
        image_name: 镜像名称

    Returns:
        None
    """
    try:
        conn = Connection(to_ip, user=username, connect_kwargs={"password": password})
        conn.run('who i am')
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        print(e.args[1])
        return
    except Exception as e:
        pprint(e)
        return

    # 判断是否已经安装docker
    result = conn.run("docker --version", warn=True, hide=True)
    if result.failed:
        pprint(f"server: {to_ip} docker is not installed!")
        return

    # 从镜像仓库拉取镜像
    conn.run(f"docker pull {registries}/{image_name}")

    # 修改标签
    conn.run(f"docker tag {registries}/{image_name} {image_name}")

    # 移除原有标签
    conn.run(f"docker rmi {registries}/{image_name}")

    pprint("congratulations, docker pull complete！")


async def parse_cmd():
    # 读取command arg
    parser = argparse.ArgumentParser(prog="AutoDeploy", description='Auto Deploy, 支持docker自动部署, 镜像上传到远程服务器同时上传到镜像仓库, 镜像从远程镜像仓库下载到本地',
                                     usage='python %(prog)s.py [options]\n '
                                           'example: \n'
                                           '自动化部署docker: python %(prog)s.py -i localhost -l E:\\ANDY\\docker -r /home/docker -p passowrd \n'
                                           '自动化上传镜像: python %(prog)s.py -i localhost -f 2 -l E:\\ANDY\\docker -r /home/docker -p passowrd -ri localhost:5000 \n'
                                           '自动化拉取镜像: python %(prog)s.py -i localhost -f 3 -p passowrd -ri localhost:5000 -n rhapsody:latest')
    parser.add_argument('--ips', type=str, help='远程服务器ip地址,多个ip请使用空格分割', default="localhost")
    parser.add_argument('-f', '--funcations', type=int, choices=[1, 2, 3], help='选择要使用的功能', required=True, default=1)
    parser.add_argument('-l', '--local_dir', type=str, help='本地文件夹完整路径', default=".")
    parser.add_argument('-r', '--remote_dir', type=str, help='远程服务器的目标路径', default="/home/docker")
    parser.add_argument('-u', '--username', type=str,
                        help='远程服务器用户名', default="root")
    parser.add_argument('-p', '--password', type=str, help='远程服务器用户名对应的密码', required=True)
    parser.add_argument('-i', '--docker_info', type=str, help='docker压缩包的版本信息', default="docker-24.0.7.tgz")
    parser.add_argument('-n', '--image_name', type=str, help='容器镜像名称,多个请使用空格隔开')
    parser.add_argument('-ri', '--registries', type=str, help='容器镜像仓库地址', default="localhost:5000")

    return parser.parse_args()


async def main():
    """
    Examples:
        自动化部署docker: python AutoDeploy.py -i localhost -l E:\\ANDY\\docker -r /home/docker -p passowrd
        自动化上传镜像: python AutoDeploy.py -i localhost -f 2 -l E:\\ANDY\\docker -r /home/docker -p passowrd -ri localhost:5000
        自动化拉取镜像: python AutoDeploy.py -i localhost -p passowrd -f 3 -ri localhost:5000 -n rhapsody:latest

Auto Deploy, 支持docker自动部署, 镜像上传到远程服务器同时上传到镜像仓库, 镜像从远程镜像仓库下载到本地
    Returns:
         None
    """
    # parse cmd
    args = await parse_cmd()
    # ips = ['172.19.1.71', ]
    # local_dir = r'E:\\ANDY\\docker'
    # remote_dir = "/home/docker"

    for ip in args.ips.split(" "):
        if args.funcations == 1:
            deploy(to_ip=ip, from_dir=args.local_dir, to_dir=args.remote_dir, docker_info=args.docker_info,
                   username=args.docker_info, password=args.password)
        elif args.funcations == 2:
            upload_image(to_ip=ip, from_dir=args.local_dir, to_dir=args.remote_dir, username=args.docker_info, password=args.password, registries=args.registries)
        elif args.funcations == 3:
            for image_name in args.image_name.split(" "):
                pull_image(to_ip=ip, username=args.username, password=args.password, registries=args.registries, image_name=image_name)
        else:
            ValueError("暂时不支持的操作")


if __name__ == '__main__':
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
