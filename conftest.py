import cursor
from jinja2 import Template
import logging
import pytest
import requests

try:
    import allure
except ImportError:
    allure = None
from datetime import datetime
from config.config import TEST_MOBILE, TEST_PASSWORD
from untils.a_read import read_excel
from untils.b_use import use_data
from untils.c_send import send_http, find_sql, delete_sql, send_sql, execute_sql
from untils.e_get import get_json

logger = logging.getLogger(__name__)


def pytest_runtest_setup(item):
    case = getattr(getattr(item, "callspec", None), "params", {}).get("case")
    if not isinstance(case, dict):
        return

    case_id = case.get("id", item.name)
    feature = case.get("feature", "")
    title = case.get("titel", item.name)
    precondition = case.get("qianzhi", "无")
    description = case.get("dd", "")
    expected = case.get("expected", "")
    priority = case.get("shunxu", "")
    detail = (
        f"用例编号：{case_id}\n"
        f"所属模块：{feature}\n"
        f"用例名称：{title}\n"
        f"优先级：{priority}\n"
        f"前置条件：{precondition}\n"
        f"测试描述：{description}\n"
        f"预期结果：{expected}"
    )

    logger.info("开始执行测试用例\n%s", detail)
    if allure is not None:
        allure.dynamic.title(f"[{case_id}] {title}")
        allure.dynamic.feature(feature or "接口测试")
        allure.dynamic.story(title)
        allure.dynamic.description(detail)


@pytest.fixture
def new_session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture
def captcha_session(new_session):
    case = next(
        (c for c in read_excel() if c["id"] == "TC_API_USER_001"),
        None,
    )
    data = use_data(case)
    resp = send_http(data, new_session)
    result = {}
    get_json(case, resp, result)
    new_session.captcha = result['Extract']
    return new_session

@pytest.fixture(scope="session")
def session_login():
    """同一 session 拉验证码 + 登录"""
    session = requests.Session()
    cap = session.get("http://localhost:3000/api/user/captcha").json()["data"]["captcha"]

    body = session.post("http://localhost:3000/api/user/login", json={
        "username": TEST_MOBILE,
        "password": TEST_PASSWORD,
        "captcha": cap,
    }).json()
    return session

@pytest.fixture
def backup_sql():
    sql = "SELECT password FROM users WHERE mobile = %s"
    sql1 = "SELECT nickname FROM users WHERE mobile = %s"
    password = send_sql(sql, (TEST_MOBILE,))
    nickname = send_sql(sql1, (TEST_MOBILE,))
    yield
    sql_back = "UPDATE users SET password = %s, nickname = %s WHERE mobile = %s"
    execute_sql(sql_back, (password, nickname, TEST_MOBILE,))


@pytest.fixture
def clear_sql(case):
    try:
        allr = {}
        case = eval(Template(str(case)).render(allr))
        data = use_data(case)
        is_success = "注册成功" in str(case.get("expected", ""))
        created_by_us = False
        if is_success:
            if find_sql(data) is not None:
                delete_sql(data)
            else:
                created_by_us = True
    except Exception as e:
        print(e)

    yield

    if created_by_us:
        delete_sql(data)

@pytest.fixture
def make_address_sql():
    sql = ("INSERT INTO address (address_id, user_id,consignee, mobile, province, city, district, address,is_default,is_deleted) "
           "VALUES (1, 417, '张三', 13800138000, '广东省', '广州市', '天河区', '地址',1,0)")
    execute_sql(sql,params = None)
    yield
    sql1 = "DELETE FROM address WHERE address_id = 1"
    execute_sql(sql1,params = None)

@pytest.fixture
def make_cart_sql():
    sql =(f"INSERT INTO cart (id, user_id, goods_id, goods_attr_id,goods_num,goods_price,selected,add_time)"
          f"VALUES (1, 417, 1, 0,1, 6999,1,'{datetime.now()}')")
    execute_sql(sql,params = None)
    yield
    sql1 = "DELETE FROM cart WHERE id = 1"
    execute_sql(sql1,params = None)

@pytest.fixture
def make_order_sql():
    execute_sql("delete from `order`")
    sql = (f"insert into `order` (order_id,order_sn,user_id,order_status,order_amount,total_amount)"
           f"VALUES (1, '20260930074098298587',417, 'PENDING', 6999, 6999)")
    execute_sql(sql,params = None)
    sql1 = (f"insert into `order` (order_id,order_sn,user_id,order_status,order_amount,total_amount)"
           f"VALUES (2, '20260930074098298589',418, 'PENDING', 6999, 6999)")
    execute_sql(sql1,params = None)
    sql2 = (f"insert into `order` (order_id,order_sn,user_id,order_status,order_amount,total_amount)"
           f"VALUES (3, '20260930074098298590',417, 'PAID', 6999, 6999)")
    execute_sql(sql2,params = None)
    sql3 = (f"insert into `order` (order_id,order_sn,user_id,order_status,order_amount,total_amount)"
           f"VALUES (4, '20260930074098298591',417, 'SHIPPED', 6999, 6999)")
    execute_sql(sql3,params = None)
    yield
    sql4 = "DELETE FROM `order` WHERE order_id IN (2, 3, 4, 5)"
    execute_sql(sql4,params = None)

@pytest.fixture
def make_shop_sql():
    sql = ("insert into cart (id,user_id,goods_id,goods_attr_id,goods_num,goods_price,selected,add_time)"
           "VALUES (1, 417, 1, 0,0, 6999,1,'2023-09-30 07:40:55')")
    execute_sql(sql,params = None)
    yield
    sql1 = "DELETE FROM cart WHERE id = 1"
    execute_sql(sql1,params = None)

