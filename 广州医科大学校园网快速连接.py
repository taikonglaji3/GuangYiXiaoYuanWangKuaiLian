import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# 创建主窗口
root = tk.Tk()
root.title("广州医科大学校园网 连接工具 v1.0")

# 定义全局变量
accounts = []
passwords = []
history_file = "history.json"
driver_path = r'E:\chromedriver-win64\chromedriver.exe'  # 指定 WebDriver 的路径
login_url = 'http://192.168.12.3'  # 替换为实际的登录网址


# 加载历史记录
def load_history():
    global accounts, passwords
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                accounts = data.get("accounts", [])
                passwords = data.get("passwords", [])
                account_combo['values'] = accounts
        except Exception as e:
            messagebox.showerror("错误", f"读取历史记录失败：{e}")
    else:
        # 如果文件不存在，创建一个空文件
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump({"accounts": [], "passwords": []}, f)


# 保存历史记录
def save_history():
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump({"accounts": accounts, "passwords": passwords}, f, ensure_ascii=False, indent=4)


# 自动填充密码
def auto_fill(event):
    selected_account = account_combo.get()
    if selected_account:
        index = accounts.index(selected_account)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, passwords[index])


# 记录账号和密码
def record_account_password():
    username = account_combo.get()
    password = password_entry.get()

    if username and password:
        if username not in accounts:
            accounts.append(username)
            passwords.append(password)
            account_combo['values'] = accounts
            save_history()
            messagebox.showinfo("成功", "账号和密码已记录")
        else:
            messagebox.showwarning("重复", "该账号已存在，请更换账号")
    else:
        messagebox.showwarning("警告", "请输入账号和密码")


# 删除账号和密码
def delete_account_password():
    selected_account = account_combo.get()

    if selected_account:
        index = account_combo.current()
        if index != -1:
            confirmed = messagebox.askyesno("确认删除", f"确定要删除账号：{selected_account}")
            if confirmed:
                accounts.pop(index)
                passwords.pop(index)
                account_combo['values'] = accounts
                account_combo.set("")
                save_history()
                messagebox.showinfo("成功", "账号和密码已删除")
        else:
            messagebox.showwarning("警告", "请选择一个账号进行删除")
    else:
        messagebox.showwarning("警告", "请选择一个账号")


# 登录功能
def login():
    username = account_combo.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("警告", "请输入账号和密码")
        return

    # 启动浏览器
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(login_url)

    # 等待页面加载
    time.sleep(1)

    # 定位输入框并输入账号和密码
    try:
        input_elements = driver.find_elements(By.CLASS_NAME, 'edit_lobo_cell')
        if len(input_elements) > 2:
            input_elements[1].send_keys(username)
            input_elements[2].send_keys(password)

            # 定位登录按钮并点击
            login_button = driver.find_element(By.CLASS_NAME, 'edit_lobo_cell')
            if login_button.is_displayed() and login_button.is_enabled():
                login_button.click()
                messagebox.showinfo("成功", "登录操作已完成")
            else:
                messagebox.showwarning("警告", "登录按钮不可见或不可点击")
        else:
            messagebox.showerror("错误", "未找到足够的输入框")
    except Exception as e:
        messagebox.showerror("错误", f"操作失败：{e}")
    finally:
        driver.quit()


# 创建界面控件
frame1 = ttk.Frame(root, padding=10)
frame1.grid(row=0, column=0, sticky="nsew")

# 账号部分
account_label = ttk.Label(frame1, text="账号：")
account_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

account_combo = ttk.Combobox(frame1)
account_combo.grid(row=0, column=1, padx=5, pady=5)

account_combo.bind("<<ComboboxSelected>>", auto_fill)  # 绑定事件

# 密码部分
password_label = ttk.Label(frame1, text="密码：")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

password_entry = ttk.Entry(frame1, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

# 按钮部分
button_frame = ttk.Frame(frame1)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

login_button = ttk.Button(button_frame, text="登录", command=login)
login_button.grid(row=0, column=0, padx=5)

record_button = ttk.Button(button_frame, text="记录账号密码", command=record_account_password)
record_button.grid(row=0, column=1, padx=5)

delete_button = ttk.Button(button_frame, text="删除账号密码", command=delete_account_password)
delete_button.grid(row=0, column=2, padx=5)

# 初始化窗口大小
root.geometry("300x200")

# 加载历史记录
load_history()

# 启动主循环
root.mainloop()
