from model import Book, BorrowedInfo
from config import db
def search_ShareBooks(keyword):
    # 在书籍数据库中根据书名、作者或关键词进行模糊查询，且管理员ID不是图书馆的书籍为用户分享的书籍
    results = Book.query.filter(((Book.book_name.like(f"%{keyword}%")) |
                                 (Book.author.like(f"%{keyword}%")) |
                                 (Book.type.like(f"%{keyword}%"))) &
                                 (Book.admin_id != "图书馆")&Book.inventory>0).all()
    return results
def is_Sharedborrowed(book_id):
    borrowed_info = BorrowedInfo.query.filter_by(book_id=book_id, is_returned=False).first()
    return borrowed_info is not None