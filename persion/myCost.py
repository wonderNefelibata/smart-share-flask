from sqlalchemy import true

from model import Money, Reader
from config import db

class MyCost(db.Model):
    reader_id = db.Column(db.String(255), primary_key=True)
    type=db.Column(db.String(255),primary_key=True)
    @staticmethod
    def mycost(reader_id):
        costinfos=Money.query.filter_by(reader_id=reader_id,is_cost=1).all()
        results=[
            {
                "time":info.time,
                "money":info.money,
                "type":info.type
            }for info in costinfos
        ]
        return results

class WaitCost(db.Model):
    reader_id = db.Column(db.String(255), primary_key=True)
    type = db.Column(db.String(255), primary_key=True)
    @staticmethod
    def waitcost(reader_id):
        costinfos = Money.query.filter_by(reader_id=reader_id, is_cost=0).all()
        results = [
            {
                "money": info.money,
                "type": info.type
            } for info in costinfos
        ]
        return results

class GoCost(db.Model):
    __tablename1__ = 'money'
    reader_id = db.Column(db.String(255), primary_key=True)
    type = db.Column(db.String(255), primary_key=True)
    money = db.Column(db.Float)
    __tablename2__='reader'
    reader_id=db.Column(db.String(255), primary_key=True)
    money=db.Column(db.Float)
    @staticmethod
    def gocost(reader_id,type):
        costinfo = Money.query.filter_by(reader_id=reader_id,type=type).first()
        if not costinfo:
            return False,"未找到您的收费记录"
        readerinfo=Reader.query.filter_by(reader_id=reader_id).first()
        moneyReader=readerinfo.money
        readerinfo.money-=costinfo.money
        if costinfo.owner!="图书馆":
            ownerinfo=Reader.query.filter_by(reader_id=costinfo.owner).first()
            moneyOwner=ownerinfo.money
            ownerinfo.money+=costinfo.money
            costinfo.is_cost=True
            db.session.commit()
            if costinfo.is_cost==1 and moneyReader-costinfo.money==readerinfo.money and moneyOwner+costinfo.money==ownerinfo.money:
                print(costinfo.is_cost)
                return True,"缴费成功!"
            else:
                return False,"缴费失败"
        else:
            costinfo.is_cost = True
            db.session.commit()
        if costinfo.is_cost == 1 and moneyReader - costinfo.money == readerinfo.money:
            return True, "缴费成功!"
        else:
            return False, "缴费失败"