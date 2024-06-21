# 服务器巡检工具

本项目是一个使用Python构建的服务器巡检工具。它允许用户连接到多个服务器，执行命令，并将输出记录到Excel文件和日志文件中。

## 功能特点

- 使用SSH连接到多个服务器。
- 在所有服务器上执行指定的命令。
- 将命令输出记录到Excel文件中。
- 在GUI中显示命令输出的最后一行。
- 保存和加载服务器配置和IP地址。
- 使用PyQt5构建的用户友好图形界面。

## 前提条件

在开始之前，请确保您已经满足以下要求：

- 在您的本地机器上安装了Python 3.x。
- 安装了以下Python包：
  - `paramiko`
  - `pandas`
  - `PyQt5`

您可以使用`pip`安装所需的包：

```bash
pip install paramiko pandas PyQt5




安装
将此仓库克隆到您的本地机器：
bash
复制代码
git clone https://github.com/yourusername/server-inspection-tool.git
导航到项目目录：
bash
复制代码
cd server-inspection-tool
运行应用程序：
bash
复制代码
python main.py
使用说明
打开应用程序。
填写用户名、密码和命令字段。
点击“导入IP”按钮，从文件中导入IP地址。
点击“提交”按钮开始巡检。
结果将显示在文本区域中，并且输出将记录到server_usage.xlsx和inspection_log.log文件中。
项目结构
main.py：运行应用程序的主脚本。
config.json：保存用户名、密码和命令的文件。
ips.json：保存IP地址的文件。
inspection_log.log：巡检结果的日志文件。
server_usage.xlsx：记录命令输出的Excel文件。
