# -*- coding: utf-8 -*-
# @File    : app.py
# @Author  : AaronJny
# @Time    : 2020/04/26
# @Desc    :
import time
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from datetime import datetime
from models import db, EbbinghausTable
from config import FlaskConfig

app = Flask(__name__)
app.config.from_object(FlaskConfig)
# 初始化数据库
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    """
    首页入口
    """
    return render_template('index.html')


@app.route('/api/tables/create/', methods=['POST'])
def create_new_table():
    """
    创建一个新的遗忘曲线记忆表
    """
    name = request.json.get('name')
    start_date_str = request.json.get('start_date')
    # 兼容python 3.6.9
    # start_date = datetime.fromisoformat(start_date_str[:10])
    timestamp = time.mktime(time.strptime(start_date_str[:10], '%Y-%m-%d'))
    start_date = datetime.fromtimestamp(timestamp)
    num_per_day = int(request.json.get('num_per_day', 2))
    total_num = int(request.json.get('total_num', 50))
    et = EbbinghausTable(name=name, start_date=start_date, num_per_day=num_per_day, total_num=total_num)
    et.add()
    ret = {
        'code': 0,
        'msg': '提交成功！'
    }
    return jsonify(ret)


@app.route('/api/tables/', methods=['GET'])
def load_all_tables():
    """
    加载并返回全部遗忘曲线记忆计划表
    """
    tables = EbbinghausTable.query.all()
    tables = [table.to_dict() for table in tables]
    ret = {
        'code': 0,
        'msg': '加载成功！',
        'tables': tables
    }
    return jsonify(ret)


@app.route('/api/table/<table_id>/')
def get_table_details(table_id):
    """
    获取表格详情

    :param table_id
    """
    table_id = int(table_id)
    et: EbbinghausTable = EbbinghausTable.query.get(table_id)
    ret = {
        'code': 0,
        'msg': '请求成功！',
        'table_data': et.table_detail()
    }
    return jsonify(ret)


@app.route('/api/table/<table_id>/delete/', methods=['GET'])
def delete_table(table_id):
    """
    删除指定表格
    :param table_id: 表格编号
    """
    table_id = int(table_id)
    et: EbbinghausTable = EbbinghausTable.query.get(table_id)
    db.session.delete(et)
    db.session.commit()
    ret = {
        'code': 0,
        'msg': '删除成功！'
    }
    return jsonify(ret)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5555)
