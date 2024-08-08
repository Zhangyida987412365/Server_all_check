import requests
from bs4 import BeautifulSoup
import pandas as pd


# 解析监控设备专用
def parse_html_to_dataframe(html_content):
    """
    解析 HTML 表格并转换为 DataFrame。

    参数:
    - html_content: str, HTML 文件的内容

    返回:
    - df: DataFrame, 表示HTML表格内容的数据框
    """
    # 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到目标表格
    table = soup.find('table', id='listForm:list')
    if not table:
        print("未能找到指定的表格。")
        return None

    # 提取表头
    headers = []
    thead = table.find('thead')
    if thead:
        headers = [th.text.strip() for th in thead.find_all('span', class_='headerText')]
    else:
        print("表头未找到。")
        return None

    # 提取表格数据
    rows = []
    tbody = table.find('tbody', id='listForm:list:tb')
    if tbody:
        for tr in tbody.find_all('tr'):
            cells = tr.find_all('td')
            row = []
            for cell in cells:
                # 提取链接文本或居中文本
                link = cell.find('a')
                if link:
                    row.append(link.text.strip())
                else:
                    center_text = cell.find('center')
                    if center_text:
                        # 如果有<div>，则提取其中的文本
                        div = center_text.find('div')
                        if div:
                            row.append(div.get_text(strip=True))
                        else:
                            row.append(center_text.get_text(strip=True))
                    else:
                        row.append(cell.get_text(strip=True))
            rows.append(row)
    else:
        print("表内容未找到。")
        return None

    # 转换为 DataFrame
    df = pd.DataFrame(rows, columns=headers)
    return df
def get_view_state_and_dynamic_ids(html):
    """
    从HTML中提取javax.faces.ViewState和动态ID

    参数:
    - html: str, HTML 页面内容

    返回:
    - view_state: str, 页面状态标识符
    - dynamic_id: str, AJAX 请求中需要的动态 ID
    """
    soup = BeautifulSoup(html, 'html.parser')

    # 提取 ViewState
    view_state_input = soup.find('input', {'name': 'javax.faces.ViewState'})
    view_state = view_state_input['value'] if view_state_input else None

    # 提取动态ID（例如 queryForm:j_id22）
    button_input = soup.find('input', {'type': 'button', 'value': '获取实时性能'})
    dynamic_id = None
    if button_input and 'onclick' in button_input.attrs:
        onclick_text = button_input['onclick']
        # 从 onClick 中提取 'queryForm:j_id22'
        if 'queryForm:j_id22' in onclick_text:
            start_index = onclick_text.find("'queryForm:j_id22':'") + len("'queryForm:j_id22':'")
            end_index = onclick_text.find("'", start_index)
            dynamic_id = onclick_text[start_index:end_index]

    return view_state, dynamic_id


def make_request(cookies, headers, aid, fsuid, device_name, sub_device_name, did, max_retries=3):
    """
    执行POST请求以获取指定设备的信息

    参数:
    - cookies: dict, 请求中使用的 cookie
    - headers: dict, 请求中使用的 header
    - aid: str, 设备的唯一标识符
    - fsuid: str, 设备的 FSUID（Functional Station Unique Identifier）
    - device_name: str, 设备名称
    - sub_device_name: str, 子设备名称
    - did: str, 设备的 DID（Device ID）
    - max_retries: int, 最大重试次数

    返回:
    - 响应文本: str, 请求的响应内容
    """
    attempt = 0
    while attempt < max_retries:
        try:
            # 发起初始GET请求以获取初始页面内容和ViewState
            initial_response = requests.get(
                'http://omms.chinatowercom.cn:9000/business/resMge/pwMge/realTimePerformanceMge/realTimeperfdata.xhtml',
                cookies=cookies,
                headers=headers,
                verify=False
            )

            # 确保请求成功
            if initial_response.status_code != 200:
                print("初始请求失败，状态码:", initial_response.status_code)
                print(initial_response.text)
                return None

            # 提取 ViewState 和动态ID
            view_state, dynamic_id = get_view_state_and_dynamic_ids(initial_response.text)

            # 确保 ViewState 和动态ID 成功提取
            if not view_state:
                print("未能提取 ViewState")
                return None
            if not dynamic_id:
                print("未能提取动态ID")
                return None

            print("提取的 ViewState:", view_state)
            print("提取的动态ID:", dynamic_id)

            # 准备请求数据
            data = {
                'AJAXREQUEST': '_viewRoot',
                'queryForm': 'queryForm',
                'queryForm:addOrEditAreaNameId': device_name,
                'queryForm:aid': aid,
                'queryForm:fsuid': fsuid,
                'queryForm:deviceName': f"{device_name}/{sub_device_name}",  # 使用主设备名称和子设备名称构建完整设备名称
                'queryForm:did': did,
                'queryForm:midName': '',
                'queryForm:mid': '',
                'queryForm:panelOpenedState': '',
                'javax.faces.ViewState': view_state,  # 使用动态提取的 ViewState
                dynamic_id: dynamic_id,  # 使用动态提取的动态ID
                'AJAX:EVENTS_COUNT': '1',
            }

            # 发起 POST 请求
            response = requests.post(
                'http://omms.chinatowercom.cn:9000/business/resMge/pwMge/realTimePerformanceMge/realTimeperfdata.xhtml',
                cookies=cookies,
                headers=headers,
                data=data,
                verify=False,
            )

            # 检查是否返回 HTTP 503 状态码
            if response.status_code == 503:
                print(f"请求返回503错误, 重试次数: {attempt + 1}")
                attempt += 1
                continue  # 继续重试

            # 确保POST请求成功
            if response.status_code != 200:
                print("POST请求失败，状态码:", response.status_code)
                return None

            return response.text

        except Exception as e:
            print(f"请求时发生异常: {e}")
            attempt += 1

    print("超过最大重试次数，仍未成功。")
    return None

#
# # 定义 cookies 和 headers
# cookies = {
#     'ULTRA_U_K': '',
#     'JSESSIONID': '2D86499AE8630D1FAEE34D9B422A035A',
#     'acctId': '100982222',
#     'uid': 'dw_tangl',
#     'route': '71cd69dd9836b51e0b6e3ff69e22e1b0',
#     'pwdaToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSRVMiLCJpc3MiOiJXUzRBIiwiZXhwIjoxNzIyOTMyMzgxLCJOQU5PU0VDT05EIjoxMTgwODU1NDk3NTcyNjkxOH0.gIdz8_kY6XRHVfX2KNwZtxCZ6OYj6lFKZ5iuOIEIznM',
#     'BIGipServerywjk_new_pool1': '308878764.10275.0000',
# }
#
# headers = {
#     'Accept': '*/*',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Origin': 'http://omms.chinatowercom.cn:9000',
#     'Proxy-Connection': 'keep-alive',
#     'Referer': 'http://omms.chinatowercom.cn:9000/business/resMge/pwMge/realTimePerformanceMge/realTimeperfdata.xhtml?fsuid=44132343801682&aid=48A752D9880825E9B08505744CFC795E&aname=%25E6%2583%25A0%25E5%25B7%259E%25E5%2590%2589%25E9%259A%2586%25E4%25B8%258B%25E4%25B8%259C%25E6%25B4%25B2%25E8%25A5%25BFDC-HFH',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
# }
#
# # 调用请求函数
# response_text = make_request(
#     cookies=cookies,
#     headers=headers,
#     aid='48A752D9880825E9B08505744CFC795E',
#     fsuid='44132343801682',
#     device_name='惠州吉隆下东洲西DC-HFH',
#     sub_device_name='一体化机柜1/模块化开关电源2',  # 添加子设备名称参数
#     did='44132340601766'
# )
#
# # 打印结果
# if response_text:
#     print("请求成功，响应内容如下：")
#     # print(response_text)
# else:
#     print("请求失败或未返回数据。")
