from jinja2 import Template
import pytest
from untils.b_use import use_data
from untils.a_read import read_excel
from untils.c_send import send_http, execute_sql
from untils.d_asserts import asserts_http, asserts_sql_address

data = read_excel()
data_shop = [item for item in data if item.get('mark') == 'address']

class Test_address :
    all = {}
    @pytest.mark.parametrize("case",data_shop)
    def test_address(self,case,session_login,make_address_sql):
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
            if case['json'] is not None:
                asserts_sql_address(case)
                if r.json()['data'] == '添加成功':
                    sql1 = "DELETE FROM address WHERE consignee = '张三'"
                    execute_sql(sql1, params=None)


