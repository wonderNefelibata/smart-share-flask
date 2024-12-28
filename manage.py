from flask import Flask, jsonify, request
from flask_cors import CORS
from app import app
from manager.bookManage import BookManage
from manager.dataManage import DataManage
from manager.readerManage import ReaderManage
from manager.infoManage import InfoManage
from manager.setManage import Setting


# 获取图书列表 ok
@app.route('/admin/getBook', methods=['GET'])
def getBookList():
    book_list = BookManage.getBookList()
    return jsonify({"data": book_list, "code": 200})

# 图书编辑 ok
@app.route('/admin/book/edit', methods=['GET'])
def book_edit():
    admin_id = request.args.get('admin_id')
    picture = request.args.get('picture')
    book_name = request.args.get('name')
    author = request.args.get('writer')
    publisher = request.args.get('press')
    book_id = request.args.get('code')
    publish_time = request.args.get('date')
    type = request.args.get('type')
    source = request.args.get('source')
    inventory = request.args.get('stock')
    price = request.args.get('price')
    update_book = BookManage.updateBook(admin_id,picture,book_name,author,publisher,publish_time,book_id,type,source,inventory,price)
    return jsonify({"data": update_book, "code": 200})

# 图书删除 ok
@app.route('/admin/book/del', methods=['GET'])
def book_del():
    admin_id = request.args.get('admin_id')
    type = request.args.get('type')
    book_id = request.args.get('book_id')
    del_book=BookManage.delBook(admin_id,type,book_id)
    return jsonify({"data": del_book, "code": 200})

# 图书新增 ok
@app.route('/admin/book/add', methods=['GET'])
def book_add():
    admin_id = request.args.get('admin_id')
    picture = request.args.get('picture')
    book_name = request.args.get('name')
    author = request.args.get('writer')
    publisher = request.args.get('press')
    book_id = request.args.get('code')
    publish_time = request.args.get('date')
    type = request.args.get('type')
    source = request.args.get('source')
    inventory = request.args.get('stock')
    price = request.args.get('price')
    new_book=BookManage.addBook(admin_id,picture,book_name,author,publisher,publish_time,book_id,type,source,inventory,price)
    return jsonify({"data": new_book, "code": 200})

# 图书查询（关键字）  stay
@app.route('/admin/book/search', methods=['GET'])
def book_search():
    admin_id = request.args.get('admin_id')
    keywords = request.args.get('keywords')
    book_list = BookManage.serchBook(admin_id,keywords)
    return jsonify({"data": book_list, "code": 200})




# 获取用户列表 ok
@app.route('/admin/getReader', methods=['GET'])
def getReader():
    reader_list = ReaderManage.getReaderList()
    return jsonify({"data": reader_list, "code": 200})

# 新增用户  ok
@app.route('/admin/reader/add', methods=['GET'])
def reader_add():
    admin_id = request.args.get('admin_id')
    reader_id = request.args.get('reader_id')
    name = request.args.get('name')
    number = request.args.get('number')
    phone = request.args.get('phone')
    email = request.args.get('email')
    identity = request.args.get('identity')
    if(identity=='老师'):
        identity_check = 0
    else:
        identity_check = 1
    money = request.args.get('balance')
    new_reader = ReaderManage.addReader(admin_id, reader_id, name, number,phone,email,identity_check,money)
    return jsonify({"data": new_reader, "code": 200})

# 删除用户 ok
@app.route('/admin/reader/del', methods=['GET'])
def reader_del():
    admin_id = request.args.get('admin_id')
    reader_id = request.args.get('reader_id')
    del_reader = ReaderManage.delReader(admin_id, reader_id)
    return jsonify({"data": del_reader, "code": 200})

# 编辑用户（设置为管理员） ok
@app.route('/admin/reader/setAdmin', methods=['GET'])
def reader_setAdmin():
    admin_id = request.args.get('admin_id')
    reader_id = request.args.get('reader_id')
    update_reader = ReaderManage.updateReader(admin_id, reader_id)
    return jsonify({"data": update_reader, "code": 200})

# 查询用户（关键字）  stay
@app.route('/admin/reader/search', methods=['GET'])
def reader_search():
    admin_id = request.args.get('admin_id')
    keywords = request.args.get('keywords')
    reader_list = ReaderManage.serchReader(admin_id,keywords)
    return jsonify({"data": reader_list, "code": 200})





# 获取公告列表  ok
@app.route('/admin/getAnnouncement', methods=['GET'])
def getAnnouncement():
    info_list = InfoManage.getInfoList()
    return jsonify({"data": info_list, "code": 200})

# 新增公告  ok
@app.route('/admin/announcement/add', methods=['GET'])
def announcement_add():
    admin_id = request.args.get('admin_id')
    title = request.args.get('title')
    information = request.args.get('content')
    status = request.args.get('publish')
    if status == "发布":
        status_check = 1
    else:
        status_check = 0
    new_info = InfoManage.addInfo(admin_id, title, information, status_check)
    return jsonify({"data": new_info, "code": 200})

# 删除公告  ok
@app.route('/admin/announcement/del', methods=['GET'])
def announcement_del():
    admin_id = request.args.get('admin_id')
    info_id = request.args.get('announcement_id')
    del_info = InfoManage.delInfo(admin_id, info_id)
    return jsonify({"data": del_info, "code": 200})

# 编辑公告 ok
@app.route('/admin/announcement/edit', methods=['GET'])
def announcement_edit():
    admin_id = request.args.get('admin_id')
    info_id = request.args.get('announcement_id')
    title = request.args.get('title')
    information = request.args.get('content')
    status = request.args.get('publish')
    if status == "发布":
        status_check = True
    else:
        status_check = False
    update_info = InfoManage.updateInfo(admin_id, info_id, title, information, status_check)
    return jsonify({"data": update_info, "code": 200})

# 查询公告（关键字）  stay
@app.route('/admin/announcement/search', methods=['GET'])
def reader_search():
    admin_id = request.args.get('admin_id')
    keywords = request.args.get('keywords')
    info_list = InfoManage.serchInfo(admin_id,keywords)
    return jsonify({"data": info_list, "code": 200})




# 获取借阅量统计  ok
@app.route('/admin/chart/getData', methods=['GET'])
def chart():
    admin_id = request.args.get('admin_id')
    chart = DataManage.getData(admin_id)
    return jsonify({"data":chart, "code": 200})

# 获取饼图数据   ok
@app.route('/admin/chart/pie', methods=['GET'])
def pie():
    admin_id = request.args.get('admin_id')
    pie_data = DataManage.getTypeData(admin_id)
    return jsonify({"data":pie_data, "code": 200})



# 获取管理员个人信息  ok
@app.route('/admin/getSetting', methods=['GET'])
def getSetting():
    admin_id = request.args.get('admin_id')
    setting = Setting.getSet(admin_id)
    return jsonify({"data":setting, "code": 200})

# 管理员资料修改  ok
@app.route('/admin/edit', methods=['GET'])
def admin_edit():
    admin_id = request.args.get('admin_id')
    name = request.args.get('name')
    phone = request.args.get('phone')
    email = request.args.get('email')
    password = request.args.get('password')
    number = request.args.get('number')
    set_admin=Setting.updateSet(admin_id,name,phone,email,password,number)
    return jsonify({"data": set_admin, "code": 200})




