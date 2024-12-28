
from model import Book, BorrowedInfo
#实现搜索全书库
def search_books(keyword):
    if keyword:  # 如果关键词存在
        # 在书籍数据库中根据书名或作者进行模糊查询
        results = Book.query.filter(((Book.book_name.like(f"%{keyword}%")) | (Book.author.like(f"%{keyword}%")))&Book.inventory>0).all()

        return results  # 返回查询结果
    else:
        return None  # 如果关键词为空，则返回空结果

    # 判断书籍是否被借阅
def is_borrowed(book_id):
    borrowed_info = BorrowedInfo.query.filter_by(book_id=book_id, is_returned=False).first()
    return borrowed_info is not None