# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

# 定义要替换的字符映射
path_char_map = {
    '/': '_',  # 替换斜杠
    '\\': '_',  # 替换反斜杠
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


def parse_html_to_dataframe_and_export(html_content, csv_file_path, target_fields=None):
    """
    解析 HTML 表格并转换为 DataFrame，然后根据条件筛选数据，并导出为 CSV 文件。

    参数:
    - html_content: 待解析的 HTML 内容
    - csv_file_path: 导出 CSV 文件的路径
    - target_fields: 需要筛选的监控点字段列表（可选，默认为 ['直流电压', '直流负载总电流', '相电压']）
    """

    # 判断csv_file_path中是否包含"监控设备"
    if "监控设备" in csv_file_path:
        filtered_df = parse_html_to_dataframe(html_content)

        # 导出到 CSV 文件
        filtered_df.to_csv(f"{csv_file_path}_有{len(filtered_df)}条记录.csv", index=False, encoding='utf-8-sig')
        print(f"已将筛选后的数据导出到 {csv_file_path}_有{len(filtered_df)}条记录.csv")
    else:
        print("文件路径中不包含'监控设备'")
        # 设置默认的 target_fields
        if target_fields is None:
            target_fields = ['直流电压', '直流负载总电流', '相电压']

        # 解析 HTML 内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 检查内容
        content_to_search = soup.get_text()
        contains_switch_power = '开关电源' in content_to_search
        contains_temperature_humidity = '温湿感' in content_to_search

        # 找到目标表格
        table = soup.find('table', id='listForm:list')
        if not table:
            print("未能找到指定的表格。")
            return

        # 提取表头
        headers = []
        thead = table.find('thead')
        if thead:
            headers = [th.text.strip() for th in thead.find_all('span', class_='headerText')]
        else:
            print("表头未找到。")
            return

        # 提取表格数据
        rows = []
        tbody = table.find('tbody', id='listForm:list:tb')
        if tbody:
            for tr in tbody.find_all('tr'):
                cells = tr.find_all('td')
                row = []
                for cell in cells:
                    # 如果单元格内有链接，则提取链接的文本
                    link = cell.find('a')
                    if link:
                        row.append(link.text.strip())
                    else:
                        # 提取居中文本内容
                        center_text = cell.find('center')
                        if center_text:
                            row.append(center_text.get_text(strip=True))
                        else:
                            row.append(cell.get_text(strip=True))
                rows.append(row)
        else:
            print("表内容未找到。")
            return

        # 转换为 DataFrame
        df = pd.DataFrame(rows, columns=headers)

        # 根据 CSV 文件路径名称的条件选择策略

        # 选择策略：根据特定字段筛选或返回所有数据
        if contains_switch_power:
            # 筛选监控点列包含指定字段的行
            filtered_df = df[df['监控点'].str.contains('|'.join(target_fields), na=False)]
            print("选择了'开关电源'相关数据。")
        elif contains_temperature_humidity:
            # 如果包含"温湿感"，则不筛选数据，返回所有内容
            filtered_df = df
            print("选择了'温湿感'相关数据。返回全部内容。")
        else:
            # 默认情况下，返回所有内容
            filtered_df = df
            print("未找到特定关键字，返回全部内容。")

        # 导出到 CSV 文件
        filtered_df.to_csv(f"{csv_file_path}_有{len(df)}条记录.csv", index=False, encoding='utf-8-sig')
        print(f"已将筛选后的数据导出到 {csv_file_path}_有{len(df)}条记录.csv")


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


def sanitize_value(value):
    """替换 value 中的路径字符为下划线"""
    for char, replacement in path_char_map.items():
        value = value.replace(char, replacement)
    return value


def make_request_with_retries(cookies, headers, aid, fsuid, station_name, value, did, max_retries=3, delay=5):
    """
    带有重试机制的请求函数
    - max_retries: 最大重试次数
    - delay: 每次重试之间的延迟（秒）
    """
    attempt = 0
    result = None
    while attempt < max_retries:
        try:
            result = make_request(cookies, headers, aid, fsuid, station_name, value, did)
            if result:  # 如果请求成功，跳出循环
                break
        except requests.exceptions.RequestException as e:
            print(f"请求失败，错误: {e}")
            if e.response.status_code == 503:
                attempt += 1
                print(f"503错误，正在重试 {attempt}/{max_retries} 次...")
                time.sleep(delay)  # 等待一段时间后重试
            else:
                break
    return result


# 定义 cookies 和 headers
cookies = {
    'Hm_lvt_f6097524da69abc1b63c9f8d19f5bd5b': '1723044351',
    'route': 'c557d6d619b6ce8d000e36efec72b3ca',
    'ULTRA_U_K': '',
    'JSESSIONID': '22FAF736FF0A71949A5144F5C5794182',
    'acctId': '100982222',
    'uid': 'dw_tangl',
    'BIGipServerywjk_new_pool1': '325655980.10275.0000',
    'loginName': 'dw_tangl',
    'fp': '4d65b18f5ba21149fa635b1cb9ed1380',
    'userOrgCode': '80441300',
    'pwdaToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSRVMiLCJpc3MiOiJXUzRBIiwiZXhwIjoxNzIzMjcxNTMwLCJOQU5PU0VDT05EIjo3Njk5NTk5Njk2MDY4MzE2fQ.Cc_quwEplkcJmoPHCK25XlR6IcQG_3Qag262RVSJxO0',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'Hm_lvt_f6097524da69abc1b63c9f8d19f5bd5b=1723044351; route=c557d6d619b6ce8d000e36efec72b3ca; ULTRA_U_K=; JSESSIONID=22FAF736FF0A71949A5144F5C5794182; acctId=100982222; uid=dw_tangl; BIGipServerywjk_new_pool1=325655980.10275.0000; loginName=dw_tangl; fp=4d65b18f5ba21149fa635b1cb9ed1380; userOrgCode=80441300; pwdaToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSRVMiLCJpc3MiOiJXUzRBIiwiZXhwIjoxNzIzMjcxNTMwLCJOQU5PU0VDT05EIjo3Njk5NTk5Njk2MDY4MzE2fQ.Cc_quwEplkcJmoPHCK25XlR6IcQG_3Qag262RVSJxO0',
    'Origin': 'http://omms.chinatowercom.cn:9000',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://omms.chinatowercom.cn:9000/business/resMge/pwMge/realTimePerformanceMge/realTimeperfdata.xhtml?fsuid=44132343801682&aid=48A752D9880825E9B08505744CFC795E&aname=%25E6%2583%25A0%25E5%25B7%259E%25E5%2590%2589%25E9%259A%2586%25E4%25B8%258B%25E4%25B8%259C%25E6%25B4%25B2%25E8%25A5%25BFDC-HFH',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}


def main(args):
    # 定义 cookies 和 headers
    cookies = {
        'Hm_lvt_f6097524da69abc1b63c9f8d19f5bd5b': '1723044351',
        'route': 'c557d6d619b6ce8d000e36efec72b3ca',
        'ULTRA_U_K': '',
        'JSESSIONID': '22FAF736FF0A71949A5144F5C5794182',
        'acctId': '100982222',
        'uid': 'dw_tangl',
        'BIGipServerywjk_new_pool1': '325655980.10275.0000',
        'loginName': 'dw_tangl',
        'fp': '4d65b18f5ba21149fa635b1cb9ed1380',
        'userOrgCode': '80441300',
        'pwdaToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSRVMiLCJpc3MiOiJXUzRBIiwiZXhwIjoxNzIzMjcxNTMwLCJOQU5PU0VDT05EIjo3Njk5NTk5Njk2MDY4MzE2fQ.Cc_quwEplkcJmoPHCK25XlR6IcQG_3Qag262RVSJxO0',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'Hm_lvt_f6097524da69abc1b63c9f8d19f5bd5b=1723044351; route=c557d6d619b6ce8d000e36efec72b3ca; ULTRA_U_K=; JSESSIONID=22FAF736FF0A71949A5144F5C5794182; acctId=100982222; uid=dw_tangl; BIGipServerywjk_new_pool1=325655980.10275.0000; loginName=dw_tangl; fp=4d65b18f5ba21149fa635b1cb9ed1380; userOrgCode=80441300; pwdaToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSRVMiLCJpc3MiOiJXUzRBIiwiZXhwIjoxNzIzMjcxNTMwLCJOQU5PU0VDT05EIjo3Njk5NTk5Njk2MDY4MzE2fQ.Cc_quwEplkcJmoPHCK25XlR6IcQG_3Qag262RVSJxO0',
        'Origin': 'http://omms.chinatowercom.cn:9000',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://omms.chinatowercom.cn:9000/business/resMge/pwMge/realTimePerformanceMge/realTimeperfdata.xhtml?fsuid=44130343801926&aid=059EED07B0F5AFB2DCEF9098D82966EF&aname=%25E7%25A7%258B%25E9%2595%25BF%25E8%258A%25B1%25E6%25A0%25B7%25E5%25B9%25B4%25E5%25AE%25B6%25E5%25A4%25A9%25E4%25B8%258B',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    # 读取 CSV 文件到 DataFrame
    file_path = r'I:\pycharm\pycharm2022\PyCharm 2022.3.2\jbr\bin\班主任\页面\fsu_data.csv'  # 替换成你的 CSV 文件路径
    df = pd.read_csv(file_path)

    # 定义导出文件的目录
    export_dir = r'I:\pycharm\pycharm2022\PyCharm 2022.3.2\jbr\bin\班主任\页面'  # 替换成你的导出目录路径

    fsuid = '44132200000413'

    filtered_rows = df[df['站址运维ID'] == fsuid]

    # 确保只有一条匹配记录
    if len(filtered_rows) == 1:
        # 提取匹配行的数据
        aid = filtered_rows.iloc[0]['aid']
        fsuid = filtered_rows.iloc[0]['fsuid']
        station_name = filtered_rows.iloc[0]['站址']

        aid = filtered_rows.iloc[0]['aid']
        fsuid = filtered_rows.iloc[0]['fsuid']
        station_name = filtered_rows.iloc[0]['站址']
        station_id = filtered_rows.iloc[0]['站址运维ID']

        print(f"\n站址包含 '{station_name}' 的行中 aid 列的值：{aid}",
              f"站址包含 '{station_name}' 的行中 fsuid 列的值：{fsuid}",
              f"站址包含 '{station_name}' 的行中 站址 列的值：{station_name}")
        print()
        print()

        # 调用 test1.get_did_with_power_supply 函数，并传递当前的 aid 和 fsuid
        result_df_did = get_did_with_power_supply(cookies, headers, aid)
        # print(result_df_did)
        if not result_df_did.empty:
            # 遍历所有结果
            for index, row in result_df_did.iterrows():
                did = row['did']
                value = row['value']
                print(f"包含'开关电源'的did：{did}", f"包含'开关电源'的value：{value}")

                # 调用带有重试机制的请求函数处理每个 did
                result = make_request_with_retries(cookies, headers, aid, fsuid, station_name, value, did)

                # 如果请求成功，则解析结果并导出
                if result is not None:
                    value = sanitize_value(value)
                    export_path = os.path.join(export_dir, f'{value}.csv')  # 创建完整的导出路径
                    df_result = parse_html_to_dataframe_and_export(result, export_path)
                    print(f"数据已导出到: {export_path}")
                else:
                    print(f"请求失败，无法获取 {value} 的数据。")
        else:
            print("未找到包含'开关电源'的did。")
    else:
        print(f"没有找到站址包含 的唯一行，找到{len(filtered_rows)}行。")
        print(filtered_rows)
if __name__ == '__main__':
    main(0)