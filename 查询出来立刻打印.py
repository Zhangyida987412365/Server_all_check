import requests
from datetime import datetime
from translate import Translator

# 初始化翻译器
translator = Translator(to_lang="zh")

def get_ip_location(ip):
    url = "https://api.threatbook.cn/v3/ip/query"
    query = {
        "apikey": "test",  # 替换为你的微步社区API密钥
        "resource": ip
    }

    response = requests.get(url, params=query)

    if response.status_code == 200:
        try:
            data = response.json().get("data", {}).get(ip, {})
        except ValueError as e:
            print(f"JSON解码错误: {e}")
            print("响应内容:", response.text)
            return "未知来源"

        basic_info = data.get("basic", {})
        location_info = basic_info.get("location", {})

        # 构建IP来源信息
        country = location_info.get("country", "未知")
        province = location_info.get("province", "未知")
        city = location_info.get("city", "未知")
        carrier = basic_info.get("carrier", "未知")
        judgments = data.get("judgments", [])

        # 获取可疑程度
        suspicious_level = " ".join(judgments) if judgments else "无"

        # 尝试翻译地理位置信息和可疑程度，如果失败则使用原始文本
        try:
            translated_country = translator.translate(country)
        except Exception:
            translated_country = country

        try:
            translated_province = translator.translate(province)
        except Exception:
            translated_province = province

        try:
            translated_city = translator.translate(city)
        except Exception:
            translated_city = city

        try:
            translated_carrier = translator.translate(carrier)
        except Exception:
            translated_carrier = carrier

        try:
            translated_suspicious_level = translator.translate(suspicious_level)
        except Exception:
            translated_suspicious_level = suspicious_level

        ip_origin = f"{translated_country} {translated_province} {translated_city} {translated_carrier} 可疑程度: {translated_suspicious_level}"
        return ip_origin
    else:
        print("请求失败，状态码:", response.status_code)
        print("响应内容:", response.text)
        return "未知来源"

def generate_report(source_ips, attc_run):
    # 获取当前日期
    current_date = datetime.now().strftime("%Y.%m.%d")

    # 固定的攻击类型和受攻击地址
    attack_type = attc_run
    target_ip = "10.36.150.17"
    action_taken = "已对源攻击地址进行封禁处置"

    for source_ip in source_ips:
        # 获取IP来源信息
        ip_origin = get_ip_location(source_ip)

        # 生成并打印报告字符串
        report = (
            f"时间：{current_date}\n"
            f"攻击类型：{attack_type}\n"
            f"源地址：{source_ip}\n"
            f"IP来源：{ip_origin}\n"
            f"受攻击地址：{target_ip}\n"
            f"处置措施：{action_taken}\n"
            f"\n是否封禁？"
        )

        print(report)

# 定义所有的IP
# 定义所有的IP
source_ips = [
    "101.91.134.76",
    "52.230.152.181",
    "52.81.3.230",
    "52.230.152.231",
    "52.230.152.21",
    "52.230.152.213",
    "54.222.188.122",
    "52.230.152.161",
    "222.171.243.85",
    "60.188.9.29",
    "60.188.9.29",
    "222.171.243.85",
    "52.230.152.143",
    "52.230.152.114",
    "54.222.226.231",
    "54.222.226.231",
    "52.230.152.212",
    "52.80.209.236",
    "54.223.195.208",
    "54.223.195.208",
    "103.97.177.49",
    "52.230.152.41",
    "52.230.152.1",
    "52.80.45.223",
    "35.206.115.46"
]

generate_report(source_ips, '探测访问')
