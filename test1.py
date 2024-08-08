import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定义要替换的字符映射
path_char_map = {
    '/': '_',  # 替换斜杠
    '\\': '_', # 替换反斜杠
    ':': '_',  # 替换冒号
    '*': '_',  # 替换星号
    '?': '_',  # 替换问号
    '"': '_',  # 替换双引号
    '<': '_',  # 替换小于号
    '>': '_',  # 替换大于号
    '|': '_',  # 替换竖线
}



def get_view_state(response_text):
    """解析 HTML 响应文本，提取 javax.faces.ViewState 的值"""
    soup = BeautifulSoup(response_text, 'html.parser')
    view_state_input = soup.find('input', {'name': 'javax.faces.ViewState'})
    return view_state_input['value'] if view_state_input else None


def get_did_with_power_supply(cookies, headers, aid):
    """根据 aid 获取包含 '开关电源' 的第一个 did"""
    # 初始 GET 请求，获取页面
    initial_response = requests.get(
        'http://omms.chinatowercom.cn:9000/business/resMge/pwMge/realTimePerformanceMge/realTimeperfdata.xhtml',
        cookies=cookies,
        headers=headers,
        verify=False
    )

    # 提取 javax.faces.ViewState
    view_state = get_view_state(initial_response.text)

    # 构建 POST 请求数据
    data = {
        'AJAXREQUEST': '_viewRoot',
        'queryForm2': 'queryForm2',
        'queryForm2:j_id123': '',
        'queryForm2:aid': aid,
        'queryForm2:panel2OpenedState': '',
        'javax.faces.ViewState': view_state,
        'queryForm2:j_id125': 'queryForm2:j_id125',
        'AJAX:EVENTS_COUNT': '1'
    }

    # 发送 POST 请求
    response = requests.post(
        'http://omms.chinatowercom.cn:9000/business/resMge/pwMge/realTimePerformanceMge/realTimeperfdata.xhtml',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )

    # 解析 HTML 响应
    soup = BeautifulSoup(response.text, 'html.parser')
    table_listForm2 = soup.find('table', id='listForm2:list2')

    # 初始化存储结果的列表
    results = []

    # 遍历每个 tr 元素，提取第一个 td 中 input 的 id 和 value
    if table_listForm2:
        for tr in table_listForm2.find_all('tr', class_='rich-table-row'):
            # 找到第一个 td 元素中的 input 标签
            input_tag = tr.find('td').find('input', type='radio')
            if input_tag:
                input_id = input_tag.get('id')
                input_value = input_tag.get('value')

                # 检查 value 中是否包含 "开关电源"
                # if '开关电源' in input_value:
                #     results.append({'did': input_id, 'value': input_value})
                #     # 如果已经找到第一个包含 "开关电源" 的 did，则跳出循环
                #     break
                results.append({'did': input_id, 'value': input_value})
    # 将结果转换为 DataFrame
    df = pd.DataFrame(results)
    return df

