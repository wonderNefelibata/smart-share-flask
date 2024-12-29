from datetime import datetime

import cv2
import winsound
import requests
from pyzbar import pyzbar
# from sqlalchemy import func
from sqlalchemy import func, or_

from model import Book, Adminer, BorrowedInfo, Reader
from config import db

class BookManage():

    # 获取
    @staticmethod
    def getBookList():
        books_info = Book.query.all()
        bookList = [
            {
                "name": book.book_name,
                "book_code": book.book_id[1:],
                "author": book.author,
                "publisher": book.publisher,
                "publish_time": book.publish_time.strftime("%Y-%m-%d"),
                "type": book.type,
                "source": book.admin_id,
                "inventory": book.inventory,
                "price": book.price,
            } for book in books_info
        ]
        return bookList

    # 增
    @staticmethod
    def addBook(admin_id,picture,book_name, author, publisher, publish_time, book_id,type, inventory,price):
        # 检查管理员账号是否存在，若存在则新增书籍
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            existing_book = Book.query.filter_by(book_name=book_name).first()
            if existing_book:
                existing_book.inventory = existing_book.inventory + int(inventory)
                db.session.commit()
                return "库存已增加"
            new_book = Book(book_id=type+book_id,picture=picture, book_name=book_name, author=author,publisher=publisher,publish_time=publish_time,type=type,admin_id="图书馆",inventory=inventory,price=price)
            db.session.add(new_book)
            db.session.commit()
            return "书籍新增成功"
        else:
            return "管理员不存在，无法新增书籍"

    # 删
    @staticmethod
    def delBook(admin_id,type,book_id):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            book_borrowed = BorrowedInfo.query.filter_by(book_id=type+book_id).first()
            if book_borrowed:
                return "该书籍借阅中无法删除"
            else:
                book = Book.query.get(type+book_id)
                if book:

                    db.session.delete(book)
                    db.session.commit()
                    return "删除成功"
                else:
                    return "找不到指定书籍，可能已经被删除了"
        else:
            return "管理员不存在，无法删除书籍"




    # 改
    @staticmethod
    def updateBook(admin_id,picture,book_name,author,publisher,publish_time,param_book_id,type,source,inventory,price):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            print("前"+type+param_book_id)
            book = book = Book.query.filter_by(book_id=type+param_book_id).first()
            print("aaasda"+type+param_book_id)
            # book = Book.query.filter(func.substr(Book.book_id, 2) == param_book_id).first()
            if book:
                book.picture = picture
                book.book_name = book_name
                book.author = author
                book.publisher = publisher
                book.publish_time = publish_time
                book.type = type
                book.source = source
                book.inventory = inventory
                book.price = price
                db.session.commit()
                return "书籍信息更新成功"
            else:
                return "找不到指定的书籍"

        else:
            return "管理员不存在，无法更改书籍信息"




    # 查
    @staticmethod
    def serchBook(admin_id,keywords):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            # matched_books = Book.query.filter(func.lower(Book.book_name).like(f"%{keywords.lower()}%")).all()
            matched_books = Book.query.filter(
                or_(
                    func.lower(Book.book_name).like(f"%{keywords.lower()}%"),
                    func.lower(Book.author).like(f"%{keywords.lower()}%"),
                    func.lower(Book.book_id).like(f"%{keywords.lower()}%"),
                    func.lower(Book.type).like(f"%{keywords.lower()}%"),
                    func.lower(Book.publisher).like(f"%{keywords.lower()}%"),
                    func.lower(Book.publish_time).like(f"%{keywords.lower()}%"),
                )
            ).all()
            bookList = [
                {
                    "name": book.book_name,
                    "author": book.author,
                    "publisher": book.publisher,
                    "publish_time": book.publish_time.strftime("%Y-%m-%d"),
                    "type": book.type,
                    "source": book.admin_id,
                    "inventory": book.inventory,
                } for book in matched_books
            ]
            if matched_books:
                return bookList
            else:
                return "查询不到书籍"
        else:
            return "管理员不存在，无法查询书籍"



    # 扫描ISBN码获取图书信息
    @staticmethod
    def addBook_code():
        # 初始化摄像头
        global obj
        cap = cv2.VideoCapture(0)  # 参数0通常表示系统的默认摄像头


        # 设置窗口名和窗口大小
        cv2.namedWindow('Scan ISBN', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Scan ISBN', 800, 600)

        while True:
            # 从摄像头读取一帧图像
            print(333)
            _, img = cap.read()
            # 如果正确读取帧，ret为True
            # if not ret:
            #     print("Failed to grab frame")
            #     break
            # 将图像转换为灰度图
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 使用pyzbar解码图像中的条形码
            decoded_objects = pyzbar.decode(gray)
            # 设置变量
            data = "0"
            # 遍历解码对象
            for obj in decoded_objects:
                print(8)
                # 打印条形码类型和数据
                print('Type:', obj.type)
                print('Data:', obj.data.decode("utf-8"))
                data = obj.data.decode("utf-8")
                # 在条形码位置画一个矩形框
                cv2.rectangle(img, (obj.rect.left, obj.rect.top),
                              (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height), (0, 255, 0), 2)
                # 显示图像
            cv2.imshow('Scan ISBN', img)
            cv2.waitKey(1)  # 要加的两行代码
            if data != "0":
                break
        # 释放摄像头资源
        cap.release()
        # 关闭所有OpenCV窗口

        cv2.destroyAllWindows()

        # api秘钥
        key = '1aff19aa7d906c00ea1fa34bab9e7a63'
        # 构造请求的URL
        # url = 'https://api.tanshuapi.com/api/isbn/v1/index?key={}&isbn={}'.format(key, data)
        # http://api.tanshuapi.com/api/isbn/v1/index?key=&isbn=9787115545138
        url = 'http://api.tanshuapi.com/api/isbn/v1/index?key={}&isbn={}'.format(key,' 9787111692225')
        # 发送请求
        response = requests.get(url)
        # 解析返回结果
        result = response.json()
        # 返回查询结果

        # 检查返回的code是否表示成功
        if result.get('code') == 1 and result.get('msg') == '操作成功':

            url = result.get('data', {}).get('img', '')

            # 发送HTTP请求，获取图片内容
            response = requests.get(url)

            # 检查请求是否成功
            if response.status_code == 200:
                # 图片内容
                image_content = response.content

                # 找到最后一个'/'字符的位置
                last_slash_index = url.rfind('/')

                # 从字符串中提取出最后一个'/'后的前10个字符，如果'/'后不足10个字符，则提取出所有字符
                img_name = url[last_slash_index + 1: last_slash_index + 11] if last_slash_index + 11 <= len(
                    url) else url[last_slash_index + 1:]

                str=img_name+'.jpg'

                # 打开一个文件用于写入
                # with open(str, 'wb') as file:
                #     file.write(image_content)

                # windows 保存法：
                file_path = 'D:/librarycover/'+str
                with open(file_path, 'wb') as file:
                    file.write(image_content)

                print("Image downloaded successfully.")
            else:
                print("Failed to download image. Status code: {}".format(response.status_code))

            book = {
                "name": result.get('data', {}).get('title', ''),
                "book_code": result.get('data', {}).get('isbn', ''),
                "author": result.get('data', {}).get('author', ''),
                "publisher": result.get('data', {}).get('publisher', ''),
                "publish_time": result.get('data', {}).get('pubdate', ''),
                "price": result.get('data', {}).get('price', ''),
                "img": img_name
            }

        print (book)
        return book

        # return result





    @staticmethod
    def scann():
        # 打开摄像头
        cap = cv2.VideoCapture(0)

        # 设置窗口名和窗口大小
        cv2.namedWindow('Scan QR Code', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Scan QR Code', 800, 600)

        # 创建声音提示函数
        def beep():
            frequency = 2500
            duration = 1000
            winsound.Beep(frequency, duration)

        while True:
            # 读取摄像头画面
            _, frame = cap.read()

            # 转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 检测二维码
            barcodes = pyzbar.decode(gray)

            # 遍历所有检测到的二维码
            for barcode in barcodes:
                # 提取二维码的边界框坐标
                (x, y, w, h) = barcode.rect

                # 在图像中绘制二维码的边界框和文本
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, barcode.data.decode('utf-8'), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # 发出声音提示
                beep()

                # 输出扫描到的二维码内容
                print(barcode.data.decode('utf-8'))

                borrowedInfo=BorrowedInfo.query.filter_by(reader_id=barcode.data).all()
                reader=Reader.query.filter_by(reader_id=barcode.data).first()
                # db.delete(reader.receive_code)
                # db.commit()
                reader.receive_code = None
                db.session.commit()
                for borrowedInfo in borrowedInfo:
                    borrowedInfo.is_code=1
                db.session.commit()

            # 显示图像
            cv2.imshow('Scan QR Code', frame)

            # 按下ESC键退出程序
            if cv2.waitKey(1) == 27:
                break

        # 释放摄像头资源
        cap.release()

        # 关闭所有窗口
        cv2.destroyAllWindows()


