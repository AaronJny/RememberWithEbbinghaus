# -*- coding: utf-8 -*-
# @File    : config.py
# @Author  : AaronJny
# @Time    : 2020/04/26
# @Desc    :


class FlaskConfig:
    """
    flask的配置类
    """
    # 数据库配置
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_USERNAME = 'root'
    DB_PASSWORD = '123456'
    DB_NAME = 'ebbinghaus'
    # ORM配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}'.format(
        username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, db=DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
