from jinja2 import Template
import pytest
from untils.a_read import read_excel
from untils.b_use import use_data, use_goods
from untils.c_send import send_http
from untils.d_asserts import asserts_http

data = read_excel()
data_list = [item for item in data if item.get('mark') == 'list']


class Test_goods:
    all = {}
    @pytest.mark.parametrize("case",data_list)
    def test_goods(self, case):
        allr = {}
        case = eval(Template(str(case)).render(allr))
        data = use_goods(case)
        print(data)
        r = send_http(data,session=None)
        print(r.json())
        asserts_http(case,r,all)



