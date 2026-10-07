import base64
from io import BytesIO

import pytest
from jinja2 import Template

from config.config import URL
from untils.a_read import read_excel
from untils.c_send import send_http
from untils.d_asserts import asserts_http

data = read_excel()
data_upload = [item for item in data if str(item.get("id", "")).startswith("TC_API_UPLOAD_")]


class Test_upload:
    all = {}

    @pytest.mark.parametrize("case", data_upload)
    def test_upload(self, case, session_login):
        all = {}
        case = eval(Template(str(case)).render(all))

        if case["id"] == "TC_API_UPLOAD_003":
            filename, content, content_type = "test.txt", b"invalid image", "text/plain"
        elif case["id"] == "TC_API_UPLOAD_004":
            filename, content, content_type = "large.png", b"x" * (5 * 1024 * 1024 + 1), "image/png"
        else:
            filename = "avatar.png"
            content = base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jT8sAAAAASUVORK5CYII="
            )
            content_type = "image/png"

        request_data = {
            "method": case["method"],
            "url": URL + case["path"],
            "files": {"file": (filename, BytesIO(content), content_type)},
        }
        if "未登录" in str(case.get("qianzhi", "")):
            r = send_http(request_data, session=None)
        else:
            r = send_http(request_data, session_login)

        print(r.json())
        asserts_http(case, r, all)
        if case["id"] == "TC_API_UPLOAD_001":
            payload = r.json().get("data") or {}
            assert payload.get("url"), f"上传响应缺少 url: {r.json()}"
            assert payload.get("filename"), f"上传响应缺少 filename: {r.json()}"
