import requests
from bs4 import BeautifulSoup
import pandas as pd


cookies = {
    'route': 'dc094c6c61e28b45c058642efd8974e4',
    'ULTRA_U_K': '',
    'JSESSIONID': '728C085C418290F9C781877D96112023',
    'acctId': '100982222',
    'uid': 'dw_tangl',
    'Hm_lvt_f6097524da69abc1b63c9f8d19f5bd5b': '1723044351',
    'Hm_lpvt_f6097524da69abc1b63c9f8d19f5bd5b': '1723044351',
    'HMACCOUNT': 'BB3A18D27494BD33',
    'BIGipServerywjk_new_pool1': '42016172.10275.0000',
    'pwdaToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSRVMiLCJpc3MiOiJXUzRBIiwiZXhwIjoxNzIzMDQ4NDIyLCJOQU5PU0VDT05EIjo2NTk3MzcwNjc3MTA5NzYyN30.aEO3FM6G3axHv9sfYiC_IqHngooYhgFt_wUVnyb4WyA',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'route=dc094c6c61e28b45c058642efd8974e4; ULTRA_U_K=; JSESSIONID=728C085C418290F9C781877D96112023; acctId=100982222; uid=dw_tangl; Hm_lvt_f6097524da69abc1b63c9f8d19f5bd5b=1723044351; Hm_lpvt_f6097524da69abc1b63c9f8d19f5bd5b=1723044351; HMACCOUNT=BB3A18D27494BD33; BIGipServerywjk_new_pool1=42016172.10275.0000; pwdaToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSRVMiLCJpc3MiOiJXUzRBIiwiZXhwIjoxNzIzMDQ4NDIyLCJOQU5PU0VDT05EIjo2NTk3MzcwNjc3MTA5NzYyN30.aEO3FM6G3axHv9sfYiC_IqHngooYhgFt_wUVnyb4WyA',
    'Origin': 'http://omms.chinatowercom.cn:9000',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://omms.chinatowercom.cn:9000/business/resMge/pwMge/fsuMge/listFsu.xhtml',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

data = {
    'AJAXREQUEST': '_viewRoot',
    'queryForm:unitHidden': '',
    'queryForm:queryFlag': 'queryFlag',
    'queryForm:nameText': '',
    'queryForm:fsuidText': '',
    'queryForm:queryFsuClass_hiddenValue': '',
    'queryForm:registstatusText_hiddenValue': '',
    'queryForm:j_id57': '',
    'queryForm:j_id61': '',
    'queryForm:queryFactoryNameSelId_hiddenValue': '',
    'queryForm:queryWireLessSelId_hiddenValue': '',
    'queryForm:queryStaStatusSelId_hiddenValue': '2',
    'queryForm:queryStaStatusSelId': '2',
    'queryForm:queryIfEntranceSelId_hiddenValue': '',
    'queryForm:queryStaTypeSelId_hiddenValue': '',
    'queryForm:querySiteSourceSelId_hiddenValue': '',
    'queryForm:queryExistsAir_hiddenValue': '',
    'queryForm:queryDWCompanyName': '',
    'queryForm:j_id89': '',
    'queryForm:j_id93': '',
    'queryForm:queryHardwareFactoryNameSelId_hiddenValue': '',
    'queryForm:j_id100': '',
    'queryForm:queryFsuDeviceid': '',
    'queryForm:j_id107': '',
    'queryForm:j_id111': '',
    'queryForm:j_id115': '',
    'queryForm:j_id119': '',
    'queryForm:querytext': '',
    'queryForm:querytext2': '',
    'queryForm:queryCard_hiddenValue': '',
    'queryForm:queryCsta1_hiddenValue': '',
    'queryForm:queryCsta2_hiddenValue': '',
    'queryForm:queryStationName': '',
    'queryForm:queryProjectCode': '',
    'queryForm:queryProjectName': '',
    'queryForm:j_id141': '',
    'queryForm:countSizeText': '',
    'queryForm:currPageObjId': '1',  # 当前页码
    'queryForm:pageSizeText': '35',  # 每页条数
    'queryForm:panelOpenedState': '',
    'selectProvFlag': '0001934',
    'lon': '114.7999',
    'fsuNameHid': '莞山莲花地/FSU01',
    'lat': '22.84992',
    'innerIpName': '10.128.44.203',
    'aid': '6306672',
    'aname': '莞山莲花地',
    'selStatusHid': '2',
    'registstatusId': '1',
    'queryForm': 'queryForm',
    'autoScroll': '',
    'javax.faces.ViewState': 'j_id81',
    'queryForm:j_id149': 'queryForm:j_id149',
    'AJAX:EVENTS_COUNT': '1',
}

response = requests.post(
    'http://omms.chinatowercom.cn:9000/business/resMge/pwMge/fsuMge/listFsu.xhtml',
    cookies=cookies,
    headers=headers,
    data=data,
    verify=False,
)


# 初始化数据列表
all_rows = []

# 设置最大页码，假设最大页码为 196，需要根据实际情况调整
max_page = 196

# 标志位，用于确定是否添加表头
first_page = True

for page_num in range(1, max_page + 1):
    # 更新当前页码
    data['queryForm:currPageObjId'] = str(page_num)
    data['queryForm:list:itemScroller'] = str(page_num)

    # 将 data 转换为 URL 编码的格式
    data_encoded = "&".join([f"{key}={value}" for key, value in data.items()])

    # 发送 POST 请求
    response = requests.post(
        'http://omms.chinatowercom.cn:9000/business/resMge/pwMge/fsuMge/listFsu.xhtml',
        cookies=cookies,
        headers=headers,
        data=data_encoded,
        verify=False,
    )

    # 获取响应文本
    html_content = response.text

    # 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'html.parser')
    print(soup)
    # 查找 id 为 "queryForm:list" 的 table 元素
    table = soup.find('table', id='queryForm:list')

    if table:
        # 如果是第一页，提取表头信息
        if first_page:
            header_cells = table.find('thead').find_all('th')
            table_headers = [cell.get_text(strip=True) for cell in header_cells]
            first_page = False  # 已添加表头，后续不再添加

        # 查找 table 元素下的 id 为 "queryForm:list:tb" 的 tbody 元素
        tbody = table.find('tbody', id='queryForm:list:tb')
        # 临时存储当前页数据
        current_page_rows = []

        # 遍历 tbody 中的所有 tr 元素，提取每个 td 的内容
        for tr in tbody.find_all('tr'):
            cells = tr.find_all('td')
            cell_data = [cell.get_text(strip=True) for cell in cells]

            # 提取 did, aid, fsuid 信息
            did_value = tr.get('ondblclick').split("'")[1]  # 提取 did 值
            href_value = tr.find('a', href=True)['href']  # 提取 href 中的 aid 和 fsuid

            # 提取 aid 和 fsuid 值
            aid_value, fsuid_value = href_value.split("'")[1].split(',')

            # 将提取的数据和新列数据合并
            row_data = dict(zip(table_headers, cell_data))
            row_data.update({'did': did_value, 'aid': aid_value, 'fsuid': fsuid_value})

            current_page_rows.append(row_data)

        # 将当前页数据添加到总数据列表中
        all_rows.extend(current_page_rows)

        # 打印新增的记录数量
        print(f"第 {page_num} 页数据已提取完成，新增记录数: {len(current_page_rows)}")

# 使用 pandas 将数据转换为 DataFrame
df = pd.DataFrame(all_rows)

# 打印 DataFrame
print(df)

# 导出 DataFrame 为 CSV 文件
df.to_csv('fsu_data.csv', index=False, encoding='utf-8-sig')  # 使用 utf-8-sig 编码以支持中文

print("所有页面数据已导出到 fsu_data.csv 文件。")
