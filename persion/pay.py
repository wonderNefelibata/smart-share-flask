import random
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.util.SignatureUtils import verify_with_rsa


from config import db
from model import Reader


class payB:
    def pay(userId,money):
        config = AlipayClientConfig()
        config.server_url = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"
        config.app_id = 9021000136692170
        config.app_private_key = """
        -----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA1/QOUN9t6D2SDELs9J5TfRfSEyZPxHbYCLIdL3KHhxziMxfe8rVOVB6rF4io7LV6A1dDGba7LhU0sZz0P/8DVbOXJamk4eDXOFViSLvXgQGeWFhMVTjPd/6Pcja/pBzlMwZAuRvUrcRBsTGGFPkjISy0KUJl/+05tZ+yH7r0ZYyX+P+Lsk66huyZw9FhepNUNiGwDfMnJHEzurT+BIAgu16USNIhkNtjLjMMCvyJmC6SduMyJqrtqkiF5+KTOTtiokbgpLI84sxihwPEMYz91TL92+h7uTzgLtoII0RAqQjWOsNqwdXFacpKjBkuAO/ebc8QhFrc7DIgyC3R6VUUBQIDAQABAoIBAQCfY5fJYw9o0UDhYegoqE7wzksULTvEwv6ydFwMMBkNxWjC00SPmPgGKFiZVxlvFIbIvnhdGzzOR4KL8U9piJv6fkH531s+CEhxYLvY+SOXKQ2pIQq9/99JLo7LetM5msYkQeI1ffAcjPT7hpTzF+swyiDzLvm/ymTEw+iheMh3xdC4egGHGImGRpuhGx+5Xkp+CZcC89h3et8QcEY6Ro5Of7OGBPWAxgZsTtD8TBajv5bnaIuHPli65z5F5+RL9cXFBtds0465NPXCRuDpdOC6joPcfjcN5wWMrJdhq8e6C82U/+JmStSCjvmX0UsT9UyPPeYj0Agngw/LBMByk5KBAoGBAPfWsbrM+PaX3TI6JQ07S9J9VTAKZ2sAE9SGpxHFqf0ow3P88evqENS45HwAlY0Dgyaw2TTKehKM9kbfFEb726tS77vPJQ0A2+EUwJ8WZZ+YRJb88Wa7RKehOIr0IJYSWQToGyyYrPOplgYqNiSHVvrhU8l+HIKOe2Opr14JkFXhAoGBAN8QkLDrH+VQbJwhUYGzhE6O6KkqNou5ptgBs1AdrjnGLOKA5I6jyv1KXOSblBbLhOTaj4ipyKXt+wwZavv9z7ysFkL57+HykeizSXaOBDWkjkHkiaXIG7GTqHw8Q4DlUvw0AvanY06XgLncBq6bpDOKeoTDF6OZjIJEU55ZcPqlAoGAQErAlk3f89BXgFUXEYSlWbhLpge85kQB4OsBYhndzB+L/IXMmD+DGDvSgdyA7zDPD/Vmk0xHOJK6vI3YK8XgKWR9bkIBQYtMfuosQdjEig8tE+IQGW9REw8+pMVJwsSFtUEk83+ztg3zLiw7GWTGipRzcNy3NqMRnTwCkyl1+OECgYEA3KCwzBwzFwfd9OtLh8K8KUtWOgODod3FdT7xUVuZ+JDX0kx0Q9UjsDU9/esXpRg1YHoAn8Z2rA/fUA9P7uAS+WUoO6SkLFJVGNlD3xwGc9xHzEq0DqIHKjOG4SJmDfZEhykWiUn0gkZ9TteeUFOnLEdaeTfRiMIV5L6aCjQi9/UCgYEAyOYgweCVh5GlWAgWPgoof4qZhIwmAQdVSqFFTP5JLtTqPin7qXhNbX25waKPy0NNi4gg/Jr/bytze2MQpcGpHb9hdGoGdDO+TmiQokD49Q/cfc/WBNSnbeU5U8oIlBXcMUmTyRUMnhfO/MkonhCVy5UoidEovIPzl7RHaPvzNO0=
-----END RSA PRIVATE KEY-----
"""
        config.alipay_public_key = """
        -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1/QOUN9t6D2SDELs9J5TfRfSEyZPxHbYCLIdL3KHhxziMxfe8rVOVB6rF4io7LV6A1dDGba7LhU0sZz0P/8DVbOXJamk4eDXOFViSLvXgQGeWFhMVTjPd/6Pcja/pBzlMwZAuRvUrcRBsTGGFPkjISy0KUJl/+05tZ+yH7r0ZYyX+P+Lsk66huyZw9FhepNUNiGwDfMnJHEzurT+BIAgu16USNIhkNtjLjMMCvyJmC6SduMyJqrtqkiF5+KTOTtiokbgpLI84sxihwPEMYz91TL92+h7uTzgLtoII0RAqQjWOsNqwdXFacpKjBkuAO/ebc8QhFrc7DIgyC3R6VUUBQIDAQAB
-----END PUBLIC KEY-----
"""

        model = AlipayTradePagePayModel()
        model.out_trade_no = random.randint(1111111111111, 99999999999909999)
        model.total_amount = money
        model.subject = '智享图书馆付款'
        model.body = '您正在向您的账户充值'
        model.product_code = "FAST_INSTANT_TRADE_PAY"

        ali_request = AlipayTradePagePayRequest(biz_model=model)
        ali_request.notify_url = 'https://pay.alipay.com'
        ali_request.return_url = 'https://pay.alipay.com'

        client = DefaultAlipayClient(alipay_client_config=config)

        response_url = client.page_execute(ali_request, http_method='GET')
        reader=Reader.query.filter_by(reader_id=userId).first()
        reader.money=reader.money+money
        db.session.commit()
        return response_url
