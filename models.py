# -*- coding: utf-8 -*-
# @File    : models.py
# @Author  : AaronJny
# @Time    : 2020/04/26
# @Desc    :
import math
from datetime import datetime, timedelta
from loguru import logger
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EbbinghausTable(db.Model):
    """
    保存根据Ebbinghaus遗忘曲线制作的学习-复习计划表的数据表
    """

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    name = db.Column(db.String(128), nullable=False, default='', comment='计划表名称')
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='计划表开始执行日期')
    num_per_day = db.Column(db.Integer, nullable=False, default=2, comment='每天需要完成的list数量')
    total_num = db.Column(db.Integer, nullable=False, default=50, comment='全部list数量')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': (self.start_date + timedelta(days=self.total_days)).strftime('%Y-%m-%d'),
            'num_per_day': self.num_per_day,
            'total_num': self.total_num
        }
        return data

    @property
    def total_days(self):
        """
        计划持续总天数
        """
        total_days = int(math.ceil(self.total_num / self.num_per_day)) + 30
        return total_days

    def list_generator(self):
        """
        产生每日list的生成器
        """
        for start in range(1, self.total_num + 1, self.num_per_day):
            end = min(start + self.num_per_day, self.total_num + 1)
            yield list(range(start, end))

    @classmethod
    def get_lists_from_generator(cls, gen):
        """
        从生成器中提取一天的list数据
        :param gen: list生成器
        """
        try:
            x = next(gen)
        except StopIteration:
            x = None
        return x

    def table_detail(self):
        """
        根据表格信息推导出艾宾浩斯遗忘曲线复习计划详情
        :return:
        """
        result = [{} for _ in range(self.total_days)]
        list_gen = self.list_generator()
        for index, current_todo in enumerate(result):
            current_todo['index'] = index
            current_todo['date'] = (self.start_date + timedelta(days=index)).strftime('%Y-%m-%d')
            current_todo['learn'] = self.get_lists_from_generator(list_gen)
            current_todo['min30'] = current_todo['learn']
            current_todo['hour12'] = current_todo['learn']
            if current_todo['learn']:
                result[index + 1].setdefault('day1', []).extend(current_todo['learn'])
                result[index + 2].setdefault('day2', []).extend(current_todo['learn'])
                result[index + 4].setdefault('day4', []).extend(current_todo['learn'])
                result[index + 4].setdefault('day7', []).extend(current_todo['learn'])
                result[index + 15].setdefault('day15', []).extend(current_todo['learn'])
                result[index + 30].setdefault('day30', []).extend(current_todo['learn'])
        return result

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()
