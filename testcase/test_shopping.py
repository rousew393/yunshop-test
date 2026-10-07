from jinja2 import Template
import pytest

from conftest import make_shop_sql
from untils.b_use import use_data
from untils.a_read import read_excel
from untils.c_send import send_http
from untils.d_asserts import asserts_http, asserts_sql_shop

data = read_excel()
data_shop = [item for item in data if item.get('mark') == 'shop']

class Test_shop:
    all = {}
    @pytest.mark.parametrize("case",data_shop)
    def test_shop(self,case,session_login,make_shop_sql):
        all = {}
        case = eval(Template(str(case)).render(all))
        data = use_data(case)
        if '未登录' in case.get('qianzhi'):
            r = send_http(data, session=None)
            print(r.json())
            asserts_http(case,r,all)
        elif '已登录' in case.get('qianzhi'):
            r = send_http(data, session_login)
            print(r.json())
            asserts_http(case,r,all)
            if '购物车' in case.get('qianzhi'):
                if case['json']:
                    asserts_sql_shop(case)


