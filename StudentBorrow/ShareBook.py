from model import Book
from config import db
from datetime import datetime
def share_book(admin_id, book_name, author, publisher, publish_time, picture,main_type,sub_type,price,code):
        category_mapping = {
        '思想类': {'思想类': 'A'},
        '哲学宗教类': {'哲学宗教类': 'B'},
        '社会科学类': {'社会科学总论': 'C','政治法律类': 'D', '军事类': 'E', '经济类': 'F','文化科学教育体育类': 'G','语言文字类': 'H','文学类': 'I','艺术类': 'J','历史地理类': 'K'},
        '自然科学类': {'自然科学总论': 'N','数理科学和化学': '0','天文学、地球科学': 'P','生物科学': 'Q','医药、卫生': 'R','农业科学': 'S','工业技术': 'T','交通运输': 'U','航空、航天': 'V','环境科学、安全科学': 'X'},
        '综合性图书': {'综合性图书': 'Z'}
        }
        # 查找对应的字母
        type_mapping = category_mapping.get(main_type, {})
        type = type_mapping.get(sub_type, '')
        print(type_mapping)
        print(type)

        book_id=type+code
        # 创建新书籍对象
        new_book = Book(book_id=book_id, book_name=book_name, author=author, publisher=publisher,
                        publish_time=publish_time, type=type,
                        picture=picture, admin_id=admin_id, inventory=1, price=price,share_time=datetime.now())

        # 将新书籍添加到数据库
        db.session.add(new_book)
        db.session.commit()

        # return {'message': '分享成功', 'book_id': book_id}
        return {'message': '分享成功'}
