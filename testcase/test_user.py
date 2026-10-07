from jinja2 import Template
import pytest
from untils.b_use import use_data
from untils.a_read import read_excel
from untils.c_send import send_http, find_sql
from untils.d_asserts import asserts_http, asserts_sql

data = read_excel()
data_01 = [item for item in data if item.get('mark') == 'login']
data_02 = [item for item in data if item.get('mark') == 'zhuin']
data_03 = [item for item in data if item.get('mark') == 'select']


class Test_login:
    allr = {}

    @pytest.mark.parametrize("case",data_01)
    def test_login(self, case,captcha_session):
        captcha = captcha_session
        allr = {
            "Extract": captcha_session.captcha
        }
        case = eval(Template(str(case)).render(allr))
        data = use_data(case)
        print(data)
        r = send_http(data, captcha)
        print(r.json())
        asserts_http(case,r,all)

class Test_zhu:
    allr = {}
    @pytest.mark.parametrize("case",data_02)
    def test_zhu(self, case,clear_sql):
        allr ={}
        case = eval(Template(str(case)).render(allr))
        data = use_data(case)
        print(data)
        r = send_http(data,session = None)
        print(r.json())
        asserts_http(case,r,allr)
        if r.json()['code'] == 200:
            asserts_sql(data)

class Test_check:
    allr = {}
    @pytest.mark.parametrize("case",data_03)
    def test_check(self, case,session_login,backup_sql):
        allr = {
            "oldPassword": "Test@123"
        }
        case = eval(Template(str(case)).render(allr))
        data = use_data(case)
        if '未登录' in case.get('qianzhi'):
            r = send_http(data, session=None)
            print(r.json())
            asserts_http(case, r, allr)
        elif '已登录' in case.get('qianzhi'):
            r = send_http(data, session_login)
            print(r.json())
            asserts_http(case, r, allr)










