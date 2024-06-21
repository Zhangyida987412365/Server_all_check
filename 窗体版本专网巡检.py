import os
import json
import paramiko
import logging
import pandas as pd
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore

# 获取当前工作目录
current_dir = os.getcwd()

# 设置巡检日志记录器
inspection_logger = logging.getLogger('inspection_logger')
inspection_logger.setLevel(logging.INFO)

# 设置巡检日志记录器的文件处理器
log_file_path = os.path.join(current_dir, 'inspection_log.log')
inspection_handler = logging.FileHandler(log_file_path)
inspection_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
inspection_logger.addHandler(inspection_handler)

# 初始化一个空的 DataFrame
df = pd.DataFrame(columns=['时间', '主机名', '命令', '输出'])  # 修改列头为中文
ips = []

# 保存输入记录的文件路径
config_file_path = os.path.join(current_dir, 'config.json')
ips_file_path = os.path.join(current_dir, 'ips.json')

# 提取IP地址的函数
def extract_ips_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line.strip()]

def save_config(username, password, command):
    config = {
        'username': username,
        'password': password,
        'command': command
    }
    with open(config_file_path, 'w') as config_file:
        json.dump(config, config_file)

def load_config():
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as config_file:
            return json.load(config_file)
    return {}

def save_ips():
    with open(ips_file_path, 'w') as ips_file:
        json.dump(ips, ips_file)

def load_ips():
    global ips
    if os.path.exists(ips_file_path):
        with open(ips_file_path, 'r') as ips_file:
            ips = json.load(ips_file)

def run_curl_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode() + stderr.read().decode()  # 将标准输出和标准错误输出合并
    last_line = output.strip().split('\n')[-1]  # 只获取最后一行
    return last_line, output  # 返回完整输出和最后一行

def log_to_excel(server, command, output):
    global df
    log_entry = pd.DataFrame({
        '时间': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],  # 修改列头为中文
        '主机名': [server['hostname']],  # 修改列头为中文
        '命令': [command],  # 修改列头为中文
        '输出': [output]  # 修改列头为中文
    })
    df = pd.concat([df, log_entry], ignore_index=True)
    excel_file_path = os.path.join(current_dir, 'server_usage.xlsx')
    df.to_excel(excel_file_path, index=False)

class Worker(QtCore.QThread):
    log_signal = QtCore.pyqtSignal(str)
    finished_signal = QtCore.pyqtSignal()

    def __init__(self, servers, command):
        super().__init__()
        self.servers = servers
        self.command = command

    def run(self):
        for server in self.servers:
            self.check_server(server, self.command)
        self.finished_signal.emit()

    def check_server(self, server, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.log_signal.emit(f"正在连接到服务器 {server['hostname']}...")
            ssh.connect(server['hostname'], server['port'], server['username'], server['password'])
            last_line, full_output = run_curl_command(ssh, command)  # 运行命令
            self.log_signal.emit(f"{server['hostname']} 的命令输出最后一行:\n{last_line}")

            log_to_excel(server, command, full_output)  # 记录到 Excel
            inspection_logger.info(f"{server['hostname']} 的命令输出: {full_output}")  # 记录到日志

        except Exception as e:
            error_message = f"连接到服务器 {server['hostname']} 时出错: {e}"
            self.log_signal.emit(error_message)
            inspection_logger.error(error_message)
        finally:
            ssh.close()

class ServerInspectionApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('服务器巡检工具')
        self.setGeometry(100, 100, 600, 600)

        # 设置全局样式
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                font-family: Arial, sans-serif;
                color: white;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                background-color: #333;
                color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 14px;
            }
        """)

        layout = QtWidgets.QVBoxLayout()

        form_layout = QtWidgets.QFormLayout()
        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.command_input = QtWidgets.QLineEdit()

        form_layout.addRow('用户名:', self.username_input)
        form_layout.addRow('密码:', self.password_input)
        form_layout.addRow('命令:', self.command_input)

        button_layout = QtWidgets.QHBoxLayout()
        self.submit_button = QtWidgets.QPushButton('提交')
        self.import_button = QtWidgets.QPushButton('导入IP')
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.import_button)

        self.result_text = QtWidgets.QTextEdit()
        self.result_text.setReadOnly(True)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

        self.submit_button.clicked.connect(self.on_submit)
        self.import_button.clicked.connect(self.import_ips)

        # 加载上次的配置和IP记录
        config = load_config()
        if config:
            self.username_input.setText(config.get('username', ''))
            self.password_input.setText(config.get('password', ''))
            self.command_input.setText(config.get('command', ''))

        load_ips()

    def log_message(self, message):
        self.result_text.append(message)
        self.result_text.verticalScrollBar().setValue(self.result_text.verticalScrollBar().maximum())

    def on_finished(self):
        QtWidgets.QMessageBox.information(self, "完成", "检查完成")

    def on_submit(self):
        username = self.username_input.text()
        password = self.password_input.text()
        command = self.command_input.text()

        if not username or not password or not command:
            QtWidgets.QMessageBox.warning(self, "输入错误", "请填写所有字段")
            return

        if not ips:
            QtWidgets.QMessageBox.warning(self, "IP地址错误", "请先导入IP地址")
            return

        # 保存输入记录
        save_config(username, password, command)
        # 初始化 Excel 文件，添加标题行
        excel_file_path = os.path.join(current_dir, 'server_usage.xlsx')
        df.to_excel(excel_file_path, index=False)

        # 创建后台任务
        servers = [{'hostname': ip, 'port': 22, 'username': username, 'password': password} for ip in ips]
        self.worker = Worker(servers, command)
        self.worker.log_signal.connect(self.log_message)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def import_ips(self):
        global ips
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择IP文件", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            try:
                ips = extract_ips_from_file(file_path)
                save_ips()
                QtWidgets.QMessageBox.information(self, "成功", f"已导入 {len(ips)} 个IP地址")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "错误", f"导入IP地址时出错: {e}")

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ServerInspectionApp()
    window.show()
    sys.exit(app.exec_())
