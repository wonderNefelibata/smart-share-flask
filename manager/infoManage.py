from datetime import datetime
from sqlalchemy import func, or_
from model import Information, Adminer
from config import db

class InfoManage():

    # 获取
    @staticmethod
    def getInfoList():
        infos = Information.query.all()
        infoList = [
            {
                "info_id": info.info_id,
                "title": info.title,
                "information": info.information,
                "status": "已发布" if info.status == 1 else "未发布",
                "create_time": info.create_time,
                "public_time": info.public_time,
            } for info in infos
        ]
        return infoList

    # 增
    @staticmethod
    def addInfo(admin_id,title, information, status):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            existing_info = Information.query.filter_by(title=title).first()
            if existing_info:
                return "该标题已存在，请重新输入"
            # create_time=datetime.now()
            max_id = db.session.query(db.func.max(Information.info_id)).scalar()
            new_id = max_id + 1 if max_id is not None else 1
            if status == 1:
                public_time=datetime.now()
            else:
                public_time= None
            new_info = Information(
                info_id=new_id,
                adminer_id=admin_id,
                title=title,
                information=information,
                status=status,
                create_time=datetime.now(),
                public_time=public_time)
            db.session.add(new_info)
            db.session.commit()
            return "公告新增成功"
        else:
            return "管理员不存在，无法新增公告"

    # 删
    @staticmethod
    def delInfo(admin_id,info_id):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            info = Information.query.get(info_id)
            if info:
                db.session.delete(info)
                db.session.commit()
                return "该公告已删除"
            else:
                return "找不到指定公告"
        else:
            return "管理员不存在，无法删除公告"

    # 改
    @staticmethod
    def updateInfo(admin_id, info_id, title, information, status):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            if status == True:
                public_time = datetime.now()
            else:
                public_time = None
            Info = Information.query.get(info_id)
            if Info:
                Info.title = title
                Info.information = information
                Info.status = status
                Info.public_time = public_time
                db.session.commit()
                return "公告信息更新成功"
            else:
                return "找不到指定公告"
        else:
            return "管理员不存在，无法更新公告"


    # 查
    @staticmethod
    def serchInfo(admin_id,keywords):
        existing_adminId = Adminer.query.filter_by(adminer_id=admin_id).first()
        if existing_adminId:
            # Info = Information.query.get(keywords)
            matched_infos = Information.query.filter(
                or_(
                    func.lower(Information.title).like(f"%{keywords.lower()}%"),
                    func.lower(Information.information).like(f"%{keywords.lower()}%"),
                )
            ).all()
            info_list = [
                {
                    "info_id": info.info_id,
                    "title": info.title,
                    "information": info.information,
                    "status": "已发布" if info.status == 1 else "未发布",
                    "create_time": info.create_time,
                    "public_time": info.public_time,
                } for info in matched_infos
            ]
            if matched_infos:
                return info_list
            else:
                return "查询不到该公告"
        else:
            return "管理员不存在，无法查询公告"