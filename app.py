import cv2
from pyzbar import pyzbar
# import pyzbar.pyzbar as pyzbar
from datetime import datetime
# from manager.bookManage import BookManage
from model import User
from persion.pay import payB

# from persion.pay import get_ali_object


verification_code = 0
import random
# import requests

import ast
from flask import Flask, jsonify, request, url_for, redirect
from flask_cors import CORS
from config import Config, db
from manager.bookManage import BookManage
from manager.dataManage import DataManage
from manager.readerManage import ReaderManage
from manager.infoManage import InfoManage
from manager.setManage import Setting

from persion.User import forgetpassword, Register, Login
from persion.myBorrow import UsedBorrow, MyBorrow
from sqlalchemy import text
from StudentBorrow.BorrowCode import generate_borrow_qr_code
from StudentBorrow.BorrowList import add_to_borrowed_list, show_borrowed_list, add_to_Share_borrowed_list
from StudentBorrow.Favorate import recommend_books
from StudentBorrow.HotBorrow import get_popular_books
from StudentBorrow.SearchAllBook import is_borrowed, search_books
from StudentBorrow.SearchSharedBook import search_ShareBooks
from StudentBorrow.ShareBook import share_book
from StudentBorrow.ShowBook import is_me_borrowed, all_share_books, all_books
from StudentBorrow.notice import get_notices
from config import Config, db
from persion.myBorrow import UsedBorrow, MyBorrow, ReturnBorrow
from persion.User import Login, Register, forgetpassword, lookUser, change, send_verification_cod
from persion.myCost import MyCost, WaitCost, GoCost
from persion.myShare import myShare, myShareSearch


# 创建一个 Flask 应用
def create_app():
    app = Flask(__name__)
    # 跨域访问需用到的
    CORS(app)
    # 加载配置
    app.config.from_object(Config)
    # 初始化数据库
    db.init_app(app)

    @app.route('/')
    def hello_world():
        return 'login'
    
    @app.route('/db')
    def test_db():
        try:
            db.session.execute(text('SELECT 1'))  # 使用 text() 函数声明文本形式的 SQL 表达式
            return "数据库连接成功！"
        except Exception as e:
            return f"数据库连接失败：{e}"

    # 图书删除 ok
    @app.route('/admin/book/del', methods=['GET'])
    def book_del():
        admin_id = request.args.get('admin_id')
        type = request.args.get('type')
        book_id = request.args.get('book_id')
        del_book = BookManage.delBook(admin_id, type, book_id)
        return jsonify({"data": del_book, "code": 200})
    


    # app = Flask(__name__)
    # # 跨域访问需用到的
    # CORS(app)
    # # 加载配置
    # app.config.from_object(Config)
    # # 初始化数据库
    # db.init_app(app)


    # @app.route('/db')
    # def test_db():
    #     try:
    #         db.session.execute(text('SELECT 1'))  # 使用 text() 函数声明文本形式的 SQL 表达式
    #         return "数据库连接成功！"
    #     except Exception as e:
    #         return f"数据库连接失败：{e}"


    # @app.route('/')
    # def hello_world():
    #     return 'login'


    @app.route('/reader/myborrow/notCall', methods=['GET'])
    def get_unreturned_books():
        # 获取来自前端的 userId 参数
        reader_id = request.args.get('userId')

        # 调用 MyBorrow 类的 NoReturn 方法获取数据
        unreturned_books = MyBorrow.NoReturn(reader_id)

        # 将数据转换为 JSON 格式并发送回前端
        if unreturned_books:
            return jsonify({"data": unreturned_books, "code": 200})

        else:
            return jsonify({'message': '没有未归还的书籍'})


    @app.route('/reader/historyBorrow', methods=['GET'])
    def get_history_borrow():
        reader_id = request.args.get('userId')
        history_borrows = UsedBorrow.UsedBorrow(reader_id)
        if history_borrows:
            return jsonify({"data": history_borrows, 'code': 200})
        else:
            return jsonify({'message': '您还没有借过书'})


    @app.route('/reader/toReturn', methods=['GET'])
    def get_toReturn():
        reader_id = request.args.get('userId')
        bookName = request.args.get('bookName')
        is_lost = request.args.get('is_lost')
        print(is_lost)
        toReturn = ReturnBorrow.ReturnBorrow(reader_id, bookName, is_lost)
        return jsonify({'data': toReturn, 'code': 200})


    @app.route('/main', methods=['GET'])
    def login():
        username = request.args.get('reader_id')
        password = request.args.get('password')
        user = Login.login(username, password)
        if user is not None:
            return jsonify({'data': '登录成功', 'code': 200})

        else:
            print(username)
            print(password)
            return jsonify({'data': '用户名或密码错误'})


    @app.route('/register', methods=['GET'])
    def register():
        username = request.args.get('reader_id')
        password = request.args.get('password')
        rePassword = request.args.get('rePassword')
        code = request.args.get('code')
        phone = request.args.get('phone')
        email = request.args.get('email')
        identity = request.args.get('identity')
        if code == str(verification_code):
            new_user, message = Register.register(username, password, rePassword, code, phone, email, identity)
            if new_user:
                return jsonify({'data': message, 'code': 200})
            else:
                return jsonify({'data': message})
        else:
            return jsonify({'data': '验证码错误'})


    @app.route('/reader/generateCode', methods=['GET'])
    def generate_code():
        phone = request.args.get('phone')
        username = request.args.get('reader_id')

        global verification_code
        verification_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
        send_verification_cod.send_verification_code(phone, verification_code)
        return jsonify({'data': '发送成功', 'code': 200})


    @app.route('/register/forget/resetpassword', methods=['GET'])
    def reset_password():
        password = request.args.get('password')
        rePassword = request.args.get('rePassword')
        phone = request.args.get('phone')
        code = request.args.get('code')
        if code == str(verification_code):
            user, message = forgetpassword.forgetpassword(phone, password, rePassword)
            if user:
                return jsonify({'data': message, 'code': 200})
            else:
                return jsonify({'data': message})
        else:
            return jsonify({'data': '验证码错误'})


    @app.route('/reader/updateUserMsg', methods=['GET'])
    def updateUserMsg():
        username = request.args.get('userId')
        phone = request.args.get('phone')
        email = request.args.get('email')
        password = request.args.get('password')
        existing_phone = User.query.filter_by(phone=phone).first()
        if existing_phone:
            return jsonify({'type': '修改失败！', 'content': '该手机号已绑定其他账号，请更换'})
        if change.change(username, password, phone, email):
            return jsonify({"code": 200, "data": {
                "type": "修改成功！",
                "content": ""
            }, })
        else:
            return jsonify({"data": {
                "type": "修改失败！",
                "content": "邮箱格式错误"
            }})


    @app.route('/reader/myCostHistory', methods=['GET'])
    def get_myCostHistory():
        reader_id = request.args.get('userId')
        myCostHistory = MyCost.mycost(reader_id)
        return jsonify({'data': myCostHistory, 'code': 200})


    @app.route('/reader/myCostWait', methods=['GET'])
    def get_myCostWait():
        reader_id = request.args.get('userId')
        waitcost = WaitCost.waitcost(reader_id)
        return jsonify({'data': waitcost, 'code': 200})


    @app.route('/reader/toCost', methods=['GET'])
    def get_toCost():
        reader_id = request.args.get('userId')
        type = request.args.get('type')
        toCost = GoCost.gocost(reader_id, type)
        return jsonify({'data': "缴费成功", 'code': 200})


    @app.route('/userMsg', methods=['GET'])
    def get_user_msg():
        reader_id = request.args.get('userId')
        msg = lookUser.lookUser(reader_id)
        if msg:
            return jsonify({'data': msg, 'code': 200})


    @app.route('/reader/myShare', methods=['GET'])
    def get_myShare():
        reader_id = request.args.get('userId')
        myshare = myShare.myShare(reader_id)
        if myShare:
            return jsonify({'data': myshare, 'code': 200})
        else:
            return jsonify({'data': "还没分享过书籍，快去分享吧"})


    @app.route('/reader/myShareSearch', methods=['GET'])
    def get_myShareSearch():
        reader_id = request.args.get('userId')
        keyword = request.args.get('keywords')
        myshareSearch = myShareSearch.myShareSearch(reader_id, keyword)
        print(myshareSearch)
        if myShare is not None:
            return jsonify({'data': myshareSearch, 'code': 200})
        else:
            return jsonify({'data': "未找到相关结果"})


    @app.route('/reader/searchLibraryBooks', methods=['GET'])
    def get_searchLibraryBooks():
        keywords = request.args.get('keywords')
        print(keywords)
        if keywords:
            results = search_books(keywords)  # 调用搜索函数获取结果
            if results:  # 如果找到相关书籍
                # 构造返回结果
                books = []
                for book in results:
                    book_data = {
                        "img": book.picture,  # 书的封面
                        "name": book.book_name,  # 书的名字
                        "isBorrow": is_borrowed(book.book_id)  # 判断书籍是否被借阅
                    }
                    books.append(book_data)
                return jsonify({"code": 200, "data": {"books": books}})
            else:
                return jsonify({"code": 200, "data": {"books": []}})  # 如果没有查询到相关书籍，则返回空数组
        else:
            return jsonify({"code": 400, "message": "请输入关键词进行搜索"})


    # 查看公告
    @app.route('/reader/notice', methods=['GET'])
    def get_notice():
        return get_notices()


    # 进行图书借阅
    @app.route('/reader/borrowClick', methods=['GET'])
    def get_borrowClick():
        user_id = request.args.get('userId')
        if user_id:
            book_name = request.args.get('bookName')
            result = add_to_borrowed_list(user_id, book_name)
            if result == 1:
                # 借阅成功的响应
                response = {
                    "code": 200,
                    "data": {
                        "result": "借阅成功！",
                        "content": " "
                    }
                }
            elif result == 2:
                # 借阅成功的响应
                response = {
                    "code": 200,
                    "data": {
                        "result": "借阅失败！",
                        "content": "此书您已借阅且尚未归还！ "
                    }
                }
            else:
                # 借阅失败的响应
                response = {
                    "code": 200,
                    "data": {
                        "result": "借阅失败！",
                        "content": "借阅书籍数量超出限制！"
                    }
                }
            return jsonify(response)
        else:
            return redirect(url_for('login'))


    # 借阅清单（待扫码）展示
    @app.route('/reader/waitToCode', methods=['GET'])
    def get_wait_to_code():
        user_id = request.args.get('userId')
        if user_id:
            books = show_borrowed_list(user_id)
            response = {
                "code": 200,
                "data": {
                    "books": books
                }
            }
            return jsonify(response)
        else:
            return redirect(url_for('login'))


    # 生成借阅码
    @app.route('/reader/produceCode', methods=['GET'])
    def get_produceCode():
        user_id = request.args.get('userId')  # 获取用户ID
        print(user_id)
        if user_id:
            borrow_qr_code_path = generate_borrow_qr_code(user_id)  # 生成二维码借阅码路径
            if borrow_qr_code_path:
                return jsonify({'data': borrow_qr_code_path, 'code': 200})
            else:
                return jsonify({'message': 'Failed to generate borrow QR code.'}), 404


    # 分享图书
    @app.route('/reader/toShare', methods=['GET'])
    def get_toShare():
        admin_id = request.args.get('userId')
        book_name = request.args.get('name')
        author = request.args.get('author')
        publisher = request.args.get('output')
        picture = request.args.get('img')
        code = request.args.get('code')
        price = request.args.get('price')
        main_type = request.args.get('type1')
        sub_type = request.args.get('type2')
        publish_time_str = request.args.get('date')
        # 将字符串解析为 datetime 对象
        publish_time_new = datetime.strptime(publish_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        # 提取年月日部分
        publish_time = publish_time_new.strftime('%Y-%m-%d')
        # 调用分享图书功能
        result = share_book(admin_id, book_name, author, publisher, publish_time, picture, main_type, sub_type, price, code)
        if result.get('message') == "分享成功":
            # 构造固定的 JSON 格式返回
            response = {
                "code": 200,
                "message": "分享成功！",
                # "book_id": result.get('book_id')
            }
            return jsonify(response)
        else:
            return jsonify()


    # 搜索分享图书

    @app.route('/reader/searchShareBooks', methods=['GET'])
    def get_searchShareBooks():
        keywords = request.args.get('keywords')
        print(keywords)
        if keywords:
            results = search_ShareBooks(keywords)  # 调用搜索函数获取结果
            if results:
                books = []
                for book in results:
                    book_data = {
                        "img": book.picture,  # 书的封面
                        "name": book.book_name,  # 书的名字
                        "isBorrow": is_borrowed(book.book_id)  # 判断书籍是否被借阅
                    }
                    books.append(book_data)
                return jsonify({"code": 200, "data": books})
            else:
                return jsonify({"code": 200, "data": {"books": []}})  # 如果没有查询到相关书籍，则返回空数组
        else:
            return jsonify({"code": 400, "message": "请输入关键词进行搜索"})


    # 进行分享图书借阅

    # 猜你喜欢
    @app.route('/reader/like', methods=['GET'])
    def get_like():
        reader_id = request.args.get('userId')

        # 获取推荐书籍
        recommended_books = recommend_books(reader_id)

        # 构造符合指定格式的响应数据
        response_data = []
        for book in recommended_books:
            book_info = {
                'img': book.picture,  # 书籍封面
                'name': book.book_name  # 书籍名称
            }
            response_data.append(book_info)

        # 构造响应JSON
        response = {
            "code": 200,
            "data": response_data
        }

        return jsonify(response)


    # 热门借阅
    @app.route('/reader/hotBorrow', methods=['GET'])
    def get_hotBorrow():
        popular_books_info = get_popular_books()

        # 构造响应JSON
        response = {
            "code": 200,
            "data": popular_books_info
        }

        return jsonify(response)


    # 全馆书籍展示
    @app.route('/reader/getLibraryAll', methods=['GET'])
    def get_LibraryBooks():
        reader_id = request.args.get('userId')
        results = all_books()
        if results:  # 如果找到相关书籍
            # 构造返回结果
            books = []
            for book in results:
                book_data = {
                    "img": book.picture,  # 书的封面
                    "name": book.book_name,  # 书的名字
                    "isBorrow": is_me_borrowed(reader_id, book.book_id)  # 判断书籍是否被我借阅
                }
                books.append(book_data)
            return jsonify({"code": 200, "data": books})
        else:
            return jsonify({"code": 200, "data": []})  # 如果没有查询到相关书籍，则返回空数组


    # 分享书籍展示
    @app.route('/reader/getAllShare', methods=['GET'])
    def get_LibraryShareBooks():
        reader_id = request.args.get('userId')
        results = all_share_books(reader_id)
        if results:  # 如果找到相关书籍
            # 构造返回结果
            books = []
            for book in results:
                book_data = {
                    "img": book.picture,  # 书的封面
                    "name": book.book_name,  # 书的名字
                    "isBorrow": is_me_borrowed(reader_id, book.book_id)  # 判断书籍是否被我借阅
                }
                books.append(book_data)
            return jsonify({"code": 200, "data": books})
        else:
            return jsonify({"code": 200, "data": []})  # 如果没有查询到相关书籍，则返回空数组


    # 进行分享图书借阅
    @app.route('/reader/borrowShare', methods=['GET'])
    def get_borrowShareClick():
        user_id = request.args.get('userId')
        if user_id:
            book_name = request.args.get('name')
            result = add_to_Share_borrowed_list(user_id, book_name)
            if result == 1:
                # 借阅成功的响应
                response = {
                    "code": 200,
                    "data": {
                        "result": "借阅成功！",
                        "content": " "
                    }
                }
            elif result == 2:
                # 借阅成功的响应
                response = {
                    "code": 200,
                    "data": {
                        "result": "借阅失败！",
                        "content": "此书您已借阅且尚未归还！ "
                    }
                }
            else:
                # 借阅失败的响应
                response = {
                    "code": 200,
                    "data": {
                        "result": "借阅失败！",
                        "content": "借阅书籍数量超出限制！"
                    }
                }
            return jsonify(response)
        else:
            return redirect(url_for('login'))


    @app.route('/manager/scan', methods=['GET'])
    def scan():
        BookManage.scann()

        return jsonify({"code": 200, "data": '扫描成功'})


    @app.route('/pay', methods=['GET'])
    def pay():
        userId = request.args.get('userId')
        money = request.args.get('money')
        money = float(money)
        pay_url = payB.pay(userId, money)
        return jsonify({'code': 200, 'url': pay_url})
        # reader_id = request.args.get('userId')
        # money = request.args.get('money')
        # alipay = get_ali_object()
        # res = alipay.direct_pay(subject='订单：123456',  # 商品描述
        #                         out_trade_no='66666',  # 用户购买的商品订单号
        #                         total_amount = 66.6)  # 交易金额
        #
        # pay_url = f"https://openapi.alipaydev.com/gateway.do?{res}"
        #
        # # return redirect(pay_url)    # 访问是跳转到pay_url页面
        #
        #
        # return jsonify({'code': 200, 'url': pay_url})


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
        update_book = BookManage.updateBook(admin_id, picture, book_name, author, publisher, publish_time, book_id, type,
                                            source, inventory, price)
        return jsonify({"data": update_book, "code": 200})


    # # 图书删除 ok
    # @app.route('/admin/book/del', methods=['GET'])
    # def book_del():
    #     admin_id = request.args.get('admin_id')
    #     type = request.args.get('type')
    #     book_id = request.args.get('book_id')
    #     del_book = BookManage.delBook(admin_id, type, book_id)
    #     return jsonify({"data": del_book, "code": 200})


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
        inventory = request.args.get('stock')
        price = request.args.get('price')
        new_book = BookManage.addBook(admin_id, picture, book_name, author, publisher, publish_time, book_id, type,
                                    inventory, price)
        return jsonify({"data": new_book, "code": 200})


    # 图书查询（关键字）  ok
    @app.route('/admin/book/search', methods=['GET'])
    def book_search():
        admin_id = request.args.get('admin_id')
        keywords = request.args.get('keywords')
        book_list = BookManage.serchBook(admin_id, keywords)
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
        if (identity == '老师'):
            identity_check = 0
        else:
            identity_check = 1
        money = request.args.get('balance')
        new_reader = ReaderManage.addReader(admin_id, reader_id, name, number, phone, email, identity_check, money)
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


    # 查询用户（关键字）  ok
    @app.route('/admin/reader/search', methods=['GET'])
    def reader_search():
        admin_id = request.args.get('admin_id')
        keywords = request.args.get('keywords')
        reader_list = ReaderManage.serchReader(admin_id, keywords)
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


    # 查询公告（关键字）  ok
    @app.route('/admin/announcement/search', methods=['GET'])
    def info_search():
        print(222)
        admin_id = request.args.get('admin_id')
        keywords = request.args.get('keywords')
        print(111)
        info_list = InfoManage.serchInfo(admin_id, keywords)
        return jsonify({"data": info_list, "code": 200})


    # 获取借阅量统计  ok
    @app.route('/admin/chart/getData', methods=['GET'])
    def chart():
        admin_id = request.args.get('admin_id')
        chart = DataManage.getData(admin_id)
        return jsonify({"data": chart, "code": 200})


    # 获取饼图数据   ok
    @app.route('/admin/chart/pie', methods=['GET'])
    def pie():
        admin_id = request.args.get('admin_id')
        pie_data = DataManage.getTypeData(admin_id)
        return jsonify({"data": pie_data, "code": 200})


    # 获取管理员个人信息  ok
    @app.route('/admin/getSetting', methods=['GET'])
    def getSetting():
        admin_id = request.args.get('admin_id')
        setting = Setting.getSet(admin_id)
        return jsonify({"data": setting, "code": 200})


    # 管理员资料修改  ok
    @app.route('/admin/edit', methods=['GET'])
    def admin_edit():
        admin_id = request.args.get('admin_id')
        name = request.args.get('name')
        phone = request.args.get('phone')
        email = request.args.get('email')
        password = request.args.get('password')
        number = request.args.get('number')
        set_admin = Setting.updateSet(admin_id, name, phone, email, password, number)
        return jsonify({"data": set_admin, "code": 200})


    @app.route('/admin/book/add/code', methods=['GET'])
    def admin_add_code():
        result = BookManage.addBook_code()
        return jsonify(result)
    
# ===================================================================
    return app

app = create_app()


if __name__ == '__main__':
    # app = create_app()
    app.run(debug=True)
