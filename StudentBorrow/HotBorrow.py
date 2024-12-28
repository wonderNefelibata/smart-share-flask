from sqlalchemy import func

from model import BorrowedInfo, Book
from config import db
def get_popular_books():
    # 查询借阅次数最多的四本书籍
    popular_books = db.session.query(BorrowedInfo.book_id, func.count(BorrowedInfo.book_id))\
        .group_by(BorrowedInfo.book_id).order_by(func.count(BorrowedInfo.book_id).desc()).limit(4).all()

    # 获取这些书籍的详细信息
    popular_books_info = []
    for book_id, _ in popular_books:
        book = Book.query.filter_by(book_id=book_id).first()
        if book:
            book_info = {
                'img': book.picture,  # 书籍封面
                'name': book.book_name  # 书籍名称
            }
            popular_books_info.append(book_info)

    return popular_books_info