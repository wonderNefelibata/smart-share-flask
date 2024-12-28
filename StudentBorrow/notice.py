from flask import jsonify

from model import Information
# 实现获取公告列表
def get_notices():
    notices = Information.query.all()  # 查询所有公告
    if notices:  # 如果有公告
        # 构造返回结果
        notice_array = [{
            "title": notice.title,
            "content": notice.information
        } for notice in notices]
        return jsonify({"code": 200, "data": {"noticeArray": notice_array}})
    else:
        return jsonify({"code": 200, "data": {"noticeArray": []}})  # 如果没有公告，则返回空数组