import os
import re
import pandas as pd
from bs4 import BeautifulSoup

# 定义要遍历的路径
paths = [
    r'D:\360MoveData\Users\one\Desktop\日志分析记录\李学文\画册\92',
    r'D:\360MoveData\Users\one\Desktop\日志分析记录\李学文\画册\54'
]

# 定义IP地址模式
ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+\.html')

# 统计文件数量
file_count = 0

# 用于存储解析结果
results = []

# 解析HTML文件的函数
def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        # 获取IP地址
        ip_address = soup.find('span', string='IP地址：').find_next_sibling().text.strip()

        # 提取漏洞信息
        vuln_table = soup.find('tbody', id='vuln-info')
        if vuln_table:
            rows = vuln_table.find_all('tr')
            for i in range(0, len(rows), 2):
                vuln_row = rows[i]
                detail_row = rows[i + 1]
                vuln_cols = vuln_row.find_all('td')
                if len(vuln_cols) == 5:
                    vuln_name = vuln_cols[0].text.strip()
                    asset_port = vuln_cols[4].text.strip()
                    # 从详细行中提取危险等级
                    danger_level_tag = detail_row.find('span', string='危害等级:')
                    if danger_level_tag:
                        danger_level = danger_level_tag.next_sibling.strip()
                    else:
                        danger_level = '未知'  # 如果没有找到危险等级，则设为未知
                    results.append({
                        'IP': ip_address,
                        '危险等级': danger_level,
                        '漏洞名称': vuln_name,
                        '资产端口': asset_port
                    })

# 遍历路径
for path in paths:
    for root, dirs, files in os.walk(path):
        for file in files:
            if ip_pattern.match(file):
                file_count += 1
                file_path = os.path.join(root, file)
                parse_html(file_path)

# 打印统计结果
print(f"符合IP地址模式的文件总数: {file_count}")

# 创建DataFrame并保存到Excel
df = pd.DataFrame(results)
output_file = 'vuln_report.xlsx'
df.to_excel(output_file, index=False)

print(f"结果已保存到: {output_file}")
