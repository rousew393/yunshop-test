from jinja2 import Template
import pytest
from untils.b_use import use_data
from untils.a_read import read_excel
from untils.c_send import send_http, execute_sql
from untils.d_asserts import asserts_http

data = read_excel()
data_shop = [item for item in data if item.get('mark') == 'ding']

class Test_ding :
    all = {}
    @pytest.mark.parametrize("case",data_shop)
    def test_ding(self,case,session_login,make_address_sql,make_cart_sql,make_order_sql):
        all = {}
        case = eval(Template(str(case)).render(all))
        data = use_data(case)
        if '未登录' in case.get('qianzhi'):
            r = send_http(data, session=None)
            print(r.json())
            asserts_http(case,r,all)
        elif '已登录' in case.get('qianzhi'):
            if '购物车为空' in case.get('qianzhi'):
                sql = "DELETE FROM cart WHERE id = 1"
                execute_sql(sql, params=None)
            r = send_http(data, session_login)
            print(r.json())
            asserts_http(case,r,all)

