from model import Adminer, Reader
from model import User
from config import db

class Setting():

    # 获取
    @staticmethod
    def getSet(admin_id):
        if admin_id:
            admin = Adminer.query.filter_by(adminer_id=admin_id).first()
        results = {
                "name": admin.name,
                "number": admin.number,
                "email": admin.email,
            }
        return results


    # 改
    @staticmethod
    def updateSet(admin_id,name,phone,email,password,number):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            set_password = User.query.filter_by(username=admin_id).first()
            set_password.password = password
            set_password.phone = phone
            set_password.email = email
            db.session.commit()
            set = Adminer.query.filter_by(adminer_id=admin_id).first()
            set.name = name
            set.phone = phone
            set.email = email
            set.number = number
            db.session.commit()
            # set_reader = Reader.query.filter_by(reader_id=admin_id).first()
            # set_reader.name = name
            # set_reader.phone = phone
            # set_reader.email = email
            # set_reader.job_number = number
            # db.session.commit()
            return "管理员信息更新成功"
        else:
            return "管理员不存在，无法修改信息"
