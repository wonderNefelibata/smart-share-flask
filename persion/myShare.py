from flask_sqlalchemy import SQLAlchemy
from model import Book
from model import BorrowedInfo
from sqlalchemy import false

from config import db
from model import Book,Money,BorrowedInfo

class myShare(db.Model):
    adminer_id = db.Column(db.String(255), primary_key=True)
    @staticmethod
    def myShare(adminer_id):
        books=Book.query.filter_by(admin_id=adminer_id).all()
        results=[]
        if books:
            for book in books:
                borrowedInfos=BorrowedInfo.query.filter_by(book_id=book.book_id).all()
                if borrowedInfos:
                    for borrowedInfo in borrowedInfos:
                        results.append({
                            "name": borrowedInfo.book_name,
                            "author": borrowedInfo.author,
                            "output": borrowedInfo.publisher,
                            "dateShare": book.share_time,
                            "status": status(book.book_id),
                            "money": money(book.book_id)
                        })
                else:
                    results.append({
                        "name": book.book_name,
                        "author": book.author,
                        "output": book.publisher,
                        "dateShare": book.share_time,
                        "status": "未归还",
                        "money": 0
                    })

            return results
def status(book_id):
    info=BorrowedInfo.query.filter_by(book_id=book_id).one()
    if info:
        if info.is_lost==false:
            if info.is_returned == False:
                return "未归还"
            else:
                return "已归还"
        else:
            return "已丢失"

def money(book_id):
    moneys=Money.query.filter_by(book_id=book_id).all()
    RequierdNum=0
    if moneys:
        for money in moneys:
            RequierdNum+=money.money
        return RequierdNum
    else:
        return RequierdNum

class myShareSearch(db.Model):
    adminer_id = db.Column(db.String(255), primary_key=True)
    @staticmethod
    def myShareSearch(adminer_id, keyword):
        result=(myShare.myShare(adminer_id))
        results = []
        for book in result:
            if keyword in book['name'] :
                results.append(book)
        return results


