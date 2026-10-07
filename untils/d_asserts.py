import json

import jsonpath
from selenium.webdriver.common.fedcm import account

from untils.c_send import find_sql, send_sql


def asserts_http(case, r, allr=None):
    body = r.json()

    actual_code = body.get("code")
    expect_code = int(case["code"])

    assert actual_code == expect_code, (
        f"[{case.get('id')}] code 不符: 期望 {expect_code}, 实际 {actual_code}\n"
        f"响应: {body}"
    )

def asserts_sql(case):
    account = case['json']['account']
    actual = find_sql(case)
    assert actual == account

def asserts_sql_change(case):
    yuqi = case['json'][0]
    sql =f"select nickname from account where mobile = TEST_MOBILE"
    shiji = send_sql(sql)
    assert yuqi == shiji

def asserts_sql_address(case):
    n= case['json']
    name = json.loads(n).get('consignee')
    sql =f"select consignee from address where consignee = '{name}'"
    if name is not None:
        shiji = send_sql(sql)
        assert name == shiji

def asserts_sql_shop(case):
    js = case['json']
    goodsid = json.loads(js).get('goods_id')
    num = json.loads(js).get('num')
    sql =f"select goods_id from cart where goods_id = '{goodsid}'"
    sql1 = f"select goods_num from cart where goods_num = '{num}'"
    shiji = send_sql(sql)
    assert goodsid == shiji
    shiji1 = send_sql(sql1)
    assert num == shiji1



