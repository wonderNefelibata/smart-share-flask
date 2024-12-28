from model import Book
from model import BorrowedInfo
#实现搜索图书馆的书库
def all_books():
    # 获取图书库中的所有书籍
    all_books = Book.query.filter((Book.admin_id == "图书馆")&(Book.inventory>0)).all()
    return all_books

def all_share_books(reader_id):
    # 获取图书库中的所有书籍
    all_share_books = Book.query.filter((Book.admin_id != "图书馆")&(Book.inventory>0)&(Book.admin_id!=reader_id)).all()
    return all_share_books

def is_me_borrowed(reader_id,book_id):
    borrowed_info = BorrowedInfo.query.filter_by(book_id=book_id,reader_id=reader_id, is_returned=False).first()
    return borrowed_info is not None