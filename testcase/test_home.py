import pytest
from jinja2 import Template

from config.config import URL
from untils.a_read import read_excel
from untils.b_use import use_data
from untils.c_send import send_http
from untils.d_asserts import asserts_http

data = read_excel()
data_shop = [item for item in data if item.get('mark') == 'home']


@pytest.mark.parametrize("case", data_shop, ids=lambda case: case["id"])
def test_home_api(case, new_session):
    all = {}
    case = eval(Template(str(case)).render(all))
    data = use_data(case)
    r = send_http(data, session=new_session)
    body = r.json()
    asserts_http(case, r,all)
    payload = body.get("data")
    assert payload, f"[{case['id']}] data 不能为空: {body}"

    if case["id"] == "TC_API_HOME_001":
        expected_keys = {"navList", "categoryMenu", "bannerList", "floors", "hotGoods"}
        assert expected_keys.issubset(payload), f"首页数据字段不完整: {payload}"
    else:
        assert isinstance(payload, (list, dict)), f"分类菜单格式错误: {payload}"
