from model import Book
from model import Reader
from model import Adminer
from model import User
from config import db
from sqlalchemy import func, or_

class ReaderManage():

    # 获取
    @staticmethod
    def getReaderList():
        reader_info = Reader.query.all()
        readerList = [
            {
                "reader_id": reader.reader_id,
                "name": reader.name,
                "number": reader.job_number,
                "email": reader.email,
                "phone": reader.phone,
                "identity": "学生" if reader.identity == 1 else "老师",
                "money": reader.money,
                "borrowed_num": reader.borrowed_num
            } for reader in reader_info
        ]
        return readerList

    # 增
    @staticmethod
    def addReader(admin_id,reader_id,name,job_number,phone,email,identity,money):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            existing_reader = Reader.query.filter_by(reader_id=reader_id).first()
            if existing_reader:
                return "用户ID已存在，不可重复添加"
            new_user = User(username=reader_id,password="123456",is_admin=False,email=email,phone=phone)
            db.session.add(new_user)
            db.session.commit()
            new_reader = Reader(reader_id=reader_id,name=name,identity=identity,email=email,phone=phone,money=money,job_number=job_number,borrowed_num=0)
            db.session.add(new_reader)
            db.session.commit()
            return "用户添加成功"
        else:
            return "管理员不存在，无法新增用户"

    # 删
    @staticmethod
    def delReader(admin_id,reader_id):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            # user = User.query.get(reader_id)
            reader = Reader.query.get(reader_id)
            if reader:
                db.session.delete(reader)
                db.session.commit()
                user = User.query.get(reader_id)
                if user.is_admin == 1 :
                    admin = Adminer.query.get(reader_id)
                    db.session.delete(admin)
                    db.session.commit()
                db.session.delete(user)
                db.session.commit()
                return "该用户已删除"
            else:
                return "找不到该用户"
        else:
            return "管理员不存在，无法删除用户"

    # 改(设置管理员）
    @staticmethod
    def updateReader(admin_id,user_id):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            user = User.query.get(user_id)
            if user:
                admin = Adminer.query.get(user_id)
                if admin and user.is_admin == 0:
                    return "该用户已为管理员，无法重复设置"
                else:
                    user.is_admin = 1
                    db.session.commit()
                    reader = Reader.query.get(user_id)
                    new_adminer = Adminer(adminer_id=user.username, name=reader.name, email=user.email,
                                          phone=user.phone, number=reader.job_number)
                    db.session.add(new_adminer)
                    db.session.commit()
                    db.session.delete(reader)
                    db.session.commit()
                    return "已设置该用户为管理员"
            else:
                return "该用户不存在，无法设置为管理员"
        else:
            return "管理员不存在，无法更新用户信息"

    # 查
    @staticmethod
    def serchReader(admin_id,keywords):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            matched_readers = Reader.query.filter(
                or_(
                    func.lower(Reader.name).like(f"%{keywords.lower()}%"),
                    func.lower(Reader.reader_id).like(f"%{keywords.lower()}%"),
                    func.lower(Reader.borrowed_num).like(f"%{keywords.lower()}%"),
                    func.lower(Reader.email).like(f"%{keywords.lower()}%"),
                    func.lower(Reader.phone).like(f"%{keywords.lower()}%"),
                )
            ).all()
            readerList = [
                {
                    "reader_id": reader.reader_id,
                    "name": reader.name,
                    "number": reader.job_number,
                    "email": reader.email,
                    "phone": reader.phone,
                    "identity": "学生" if reader.identity == 1 else "老师",
                    "money": reader.money,
                    "borrowed_num": reader.borrowed_num
                } for reader in matched_readers
            ]
            if matched_readers:
                return readerList
            else:
                return "查询不到书籍"
        else:
            return "管理员不存在，无法查询用户"