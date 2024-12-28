import os
import random
from model import BorrowedInfo, Reader, Book
from config import db
import qrcode


def generate_borrow_qr_code(user_id):
    reader=Reader.query.filter_by(reader_id=user_id).first()
    borrowed_infos = BorrowedInfo.query.filter_by(reader_id=user_id, is_code=0).all()
    # datas = user_id+'借阅的书目有：'+'\n'
    # for borrowed_info in borrowed_infos:
    #     book = Book.query.filter_by(book_id=borrowed_info.book_id).first()
    #     name = book.book_name
    #     data = ' 一本' + name
    #     datas += data
    datas=user_id
    print(datas)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)

    qr.add_data(datas)
    qr.make(fit=True)
    imagine = qr.make_image(fill_color="black", back_color="white")  # 设置二维码颜色
    save_path = 'D:/librarycover/'
    last_path='.png'
    ran=random.randint(0, 999)
    file_name = save_path + str(ran) + last_path

    full_path = os.path.join(save_path, file_name)

    imagine.save(full_path)
    reader.receive_code=ran
    db.session.commit()
    return ran
