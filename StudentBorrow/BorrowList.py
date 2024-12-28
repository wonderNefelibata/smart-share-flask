from model import Book
from model import BorrowedInfo
from model import Money
from model import Reader
from config import db
from datetime import datetime

def add_to_borrowed_list(reader_id, book_name):
    # 检查当前用户在 BorrowedInfo 表中的借阅情况
    borrowed_books = BorrowedInfo.query.filter_by(reader_id=reader_id, is_returned=0).all()
    reader=Reader.query.filter_by(reader_id=reader_id).first()
    if reader.identity==0:
        num=10
    else:
        num=6
    # 如果当前用户已借阅的书籍数量未超过6本，则继续插入新的借阅记录
    reader.borrowed_num = len(borrowed_books)
    if len(borrowed_books) <= num:
        # book = Book.query.get(book_name=book_name)
        book = Book.query.filter_by(book_name=book_name).first()
        have_borrowed=BorrowedInfo.query.filter_by(reader_id=reader_id,book_name=book_name).all()
        if (book.inventory > 0)&(not have_borrowed or all(info.is_returned == 1 for info in have_borrowed)):
            borrowed_book = BorrowedInfo(
                reader_id=reader_id,
                book_id=book.book_id,
                book_name=book_name,
                author=book.author,
                publisher=book.publisher,
                owner_id=book.admin_id,
                borrowed_time=datetime.now().strftime("%Y-%m-%d"),
                is_returned=0,
                borrowed_num=1,
                is_code=0,
                is_lost=0,
                doer_id=27
            )
            db.session.add(borrowed_book)
            book.inventory -= 1
            reader.borrowed_num +=1
            db.session.commit()
            return 1
        else:
            return 2
    else:
        return 3  # 如果用户已经借阅了6本书，则不允许再借阅


def show_borrowed_list(reader_id):
    # 查询当前用户借阅的图书且未归还且未扫码的清单
    borrowed_books = BorrowedInfo.query.filter_by(reader_id=reader_id, is_returned=0, is_code=0).all()
    book_list = []
    for borrowed_book in borrowed_books:
        # 获取每本借阅的书籍的详情
        book = Book.query.filter_by(book_id=borrowed_book.book_id).first()
        if book:
            book_info = {
                "img": book.picture,  # 书籍封面
                "name": book.book_name  # 书籍名称
            }
            book_list.append(book_info)

    return book_list

def add_to_Share_borrowed_list(reader_id, book_name):
    # 检查当前用户在 BorrowedInfo 表中的借阅情况
    borrowed_books = BorrowedInfo.query.filter_by(reader_id=reader_id, is_returned=0).all()
    reader = Reader.query.filter_by(reader_id=reader_id).first()
    if reader.identity == 0:
        num = 10
    else:
        num = 6
    # 如果当前用户已借阅的书籍数量未超过6本，则继续插入新的借阅记录
    reader.borrowed_num = len(borrowed_books)
    if len(borrowed_books) < num:
        # book = Book.query.get(book_name=book_name)
        book = Book.query.filter_by(book_name=book_name).first()
        have_borrowed = BorrowedInfo.query.filter_by(reader_id=reader_id, book_name=book_name).all()
        if (book.inventory > 0) & (not have_borrowed or all(info.is_returned == 1 for info in have_borrowed)):
            borrowed_book = BorrowedInfo(
                reader_id=reader_id,
                book_id=book.book_id,
                book_name=book_name,
                author=book.author,
                publisher=book.publisher,
                owner_id=book.admin_id,
                borrowed_time=datetime.now().strftime("%Y-%m-%d"),
                is_returned=0,
                borrowed_num=1,
                is_code=0,
                is_lost=0,
                doer_id=27
            )
            borrow_cost = Money(
                reader_id=reader_id,
                book_id=book.book_id,
                type=book.book_name+"-借阅分享图书",
                money=book.price,
                is_cost=1,
                owner=book.admin_id,
                time=datetime.now().strftime("%Y-%m-%d"),

            )
            db.session.add(borrowed_book)
            db.session.add(borrow_cost)
            book.inventory -= 1
            reader.money += borrow_cost.money
            reader.borrowed_num += 1
            db.session.commit()
            return 1
        else:
            return 2
    else:
        return 3  # 如果用户已经借阅了6本书，则不允许再借阅

