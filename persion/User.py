import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from sqlalchemy import true

from model import User, Reader
from config import db


class Login(db.Model):
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))

    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return user
        else:
            return None


class Register(db.Model):
    username = db.Column(db.String(255), primary_key=True)
    reader = db.Column(db.String(255), primary_key=True)
    @staticmethod
    def register(username, password, rePassword, code, phone, email,identity):
        existing_user = User.query.filter_by(username=username).first()
        existing_phone = User.query.filter_by(phone=phone).first()
        if existing_phone:
            return None,'手机号已被绑定'
        if identity==1:
            identity=True
        else:
            identity=False
        if existing_user:
            return None, "用户名已经存在"
        if password != rePassword:
            return None, "两次密码不一致，请重新输入"
        new_user = User(
            username=username,
            password=password,
            is_admin=False,
            email=email,
            phone=phone)
        db.session.add(new_user)
        db.session.commit()
        newReader=Reader(
            reader_id=username,
            name='待填写',
            identity=identity,
            email=email,
            phone=phone,
            money=0,
            job_number='待填写',
            borrowed_num=0
        )
        db.session.add(newReader)
        db.session.commit()
        return new_user, "注册成功"
class send_verification_cod():
    @staticmethod
    def send_verification_code(phone_number, verification_code):
        # 阿里云API相关信息
        access_key_id = 'LTAI5tDqJpVftCezA8pnKYwm'
        access_key_secret = 'kpdtAvFZwNPWIrVzpBkR0UUvQdUdD6'
        sign_name='智享图书馆'
        template_code='SMS_465986302'
        # 初始化 AcsClient
        client = AcsClient(access_key_id, access_key_secret, 'default')

        # 创建请求
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        # 设置请求参数
        request.add_query_param('PhoneNumbers', phone_number)
        request.add_query_param('SignName', sign_name)
        request.add_query_param('TemplateCode', template_code)
        request.add_query_param('TemplateParam', '{"code":"' + str(verification_code) + '"}')

        response = client.do_action_with_exception(request)
        print(str(response, encoding='utf-8'))
        return verification_code


class forgetpassword(db.Model):
    username = db.Column(db.String(255), primary_key=True)

    @staticmethod
    def forgetpassword(phone, password, new_password):
        user = User.query.filter_by(phone=phone).first()
        if password != new_password:
            return None, "两次密码不一致"
        if user.password == password:
            return None,"与旧密码一致"
        else:
            user.password = password
            db.session.commit()
            return user, "操作成功!"
class change(db.Model):
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    @staticmethod
    def change(username, password, phone, email):
        print(username, password, phone, email)
        user = User.query.filter_by(username=username).first()
        if username:
            user.password = password
            user.phone = phone
            user.email = email
            print(email)
            if "@" in str(email):
                db.session.commit()
                reader=Reader.query.filter_by(reader_id=username).first()
                reader.email=email
                reader.phone=phone
                db.session.commit()
                return True
            else:
                return False



class lookUser(db.Model):
    reader_id = db.Column(db.Integer, primary_key=True)
    @staticmethod
    def lookUser(reader_id):
        reader=Reader.query.filter_by(reader_id=reader_id).first()
        if reader:
            results={
                    "username":reader.name,
                    "userId":reader.job_number,
                    "email":reader.email,
                    "phone":reader.phone,
                    "money":reader.money,
                    "type":type(reader.identity)
                    }
            print(reader.name)
            return results
        else:
            return None

def type(identity):
    if identity==0:
        return "学生"
    else:
        return "老师"
