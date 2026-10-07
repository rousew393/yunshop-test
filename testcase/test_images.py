import pytest

from config.config import URL
from untils.a_read import read_excel


data = [case for case in read_excel() if str(case.get("id", "")).startswith("TC_API_IMG_")]


@pytest.mark.parametrize("case", data, ids=lambda case: case["id"])
def test_image_api(case, new_session):
    response = new_session.request(case["method"], URL + case["path"])

    assert response.status_code == int(case["code"])
    assert response.content, f"[{case['id']}] 图片响应为空"
    assert response.headers.get("Content-Type", "").lower().startswith("image/"), (
        f"[{case['id']}] 响应类型不是图片: {response.headers.get('Content-Type')}"
    )
