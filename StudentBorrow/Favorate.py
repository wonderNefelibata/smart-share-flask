from model import BorrowedInfo, Book
from collections import defaultdict


def recommend_books(reader_id):
    # 查询用户借阅过的书籍
    borrowed_books = BorrowedInfo.query.filter_by(reader_id=reader_id).all()

    # 统计用户借阅过的各种类型的书籍数量
    book_type_counts = defaultdict(int)
    for borrowed_book in borrowed_books:
        book_id = borrowed_book.book_id
        book = Book.query.filter_by(book_id=book_id).first()
        if book:
            book_type = book.type
            book_type_counts[book_type] += 1

    # 找到用户借阅最多的书籍类型
    favorite_type = max(book_type_counts, key=book_type_counts.get)

    # 推荐同类书籍
    recommended_books = []
    for book in Book.query.filter_by(type=favorite_type).all():
        if len(recommended_books) < 4:
            recommended_books.append(book)
        else:
            break

    return recommended_books