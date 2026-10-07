import pytest
import os

if __name__ == "__main__":
    # 执行用例，生成allure原始数据
    pytest.main(["-vs", "./testcase", "--alluredir", "./report/json_report", "--clean-alluredir"])
    # 生成html报告
    os.system("allure generate ./report/json_report -o ./report/html_report --clean")
