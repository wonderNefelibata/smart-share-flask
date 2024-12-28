from model import BorrowedInfo, Book, Reader,Money
from config import db
from datetime import date, timedelta


class MyBorrow(db.Model):
    reader_id = db.Column(db.String(255), primary_key=True)
    book_id = db.Column(db.String(255), primary_key=True)

    @staticmethod
    def NoReturn(reader_id):
        if reader_id:
            unreturned_infos = BorrowedInfo.query.filter_by(reader_id=reader_id, is_returned=0).all()
            results = [
                {
                    "name": info.book_name,
                    "author": info.author,
                    "output": info.publisher,
                    "dateBorrow": info.borrowed_time,
                    "num": info.borrowed_num,
                    "status": change(info.is_code)
                } for info in unreturned_infos
            ]
            return results


def change(is_turned):
    if is_turned == 0:
        return "未扫码"
    else:
        return "已扫码"


class UsedBorrow(db.Model):
    reader_id = db.Column(db.String(255), primary_key=True)
    book_id = db.Column(db.String(255), primary_key=True)

    @staticmethod
    def UsedBorrow(reader_id):
        if reader_id:
            Usedinfos = BorrowedInfo.query.filter_by(reader_id=reader_id, is_returned=1).all()
            results = [
                {
                    "name": info.book_name,
                    "author": info.author,
                    "output": info.publisher,
                    "num": info.borrowed_num,
                    "dateBorrow": info.borrowed_time,
                    "dateCall": info.returned_time
                } for info in Usedinfos
            ]
            return results


class ReturnBorrow(db.Model):
    reader_id = db.Column(db.String(255), primary_key=True)
    book_id = db.Column(db.String(255), primary_key=True)

    @staticmethod
    def ReturnBorrow(reader_id, bookName,is_lost):
        print(is_lost,121312)
        if reader_id:
            returninfo = BorrowedInfo.query.filter_by(reader_id=reader_id, book_name=bookName, is_returned=0).first()
            book = Book.query.filter_by(book_name=bookName).first()
            if returninfo:
                reader=Reader.query.filter_by(reader_id=returninfo.reader_id).first()
                returninfo.is_returned = 1
                book.inventory += 1
                reader.borrowed_num -= 1
                returninfo.returned_time = date.today()
                if date.today()-returninfo.borrowed_time>timedelta(days=15):
                    print(666)
                    moneyI=Money(
                        reader_id=reader_id,
                        book_id=book.book_id,
                        money=(date.today()-returninfo.borrowed_time).days,
                        time=date.today(),
                        owner=book.admin_id,
                        is_cost=0,
                        type=book.book_name + "逾期罚款"
                    )
                    db.session.add(moneyI)
                if is_lost=='1':
                    print(1)
                    returninfo.is_lost=1
                    reader.borrowed_num -= 1
                    returninfo.returned_time =date.today()
                    moneyInfo=Money(
                        reader_id=reader_id,
                        book_id=book.book_id,
                        money = book.price,
                        time = date.today(),
                        owner = book.admin_id,
                        is_cost = 0,
                        type=book.book_name+"丢失罚款"
                    )
                    db.session.add(moneyInfo)
                db.session.commit()
                time_difference = date.today() - returninfo.borrowed_time
                if is_lost == '0':
                    if time_difference.days < 15:
                        return "归还成功"
                    else:
                        return "逾期归还，请及时缴费"
                else:
                    if time_difference.days < 15:
                        return "书本丢损，请去缴费"
                    else:
                        return "逾期归还，且已经丢损，请及时缴费"

