from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# 指定WebDriver的路径
driver_path = r'E:\chromedriver-win64\chromedriver.exe'

# 创建一个浏览器实例

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)
# 打开网页
driver.get('http://192.168.12.3')  # 替换为实

# 定位所有具有类名 'edit_lobo_cell' 的输入框
input_elements = driver.find_elements(By.CLASS_NAME, 'edit_lobo_cell')

# 选择第二个输入框并输入内容

if len(input_elements) > 2:
    input_element1 = input_elements[1]
    input_element1.send_keys('输入你的账号')
    input_element2 = input_elements[2]
    input_element2.send_keys('输入你的密码')
else:
    print("没有找到第二个这样的输入框")
login_button = driver.find_element(By.CLASS_NAME, 'edit_lobo_cell')
if login_button.is_displayed() and login_button.is_enabled():
    login_button.click()
else:
    print("按钮不可见或不可点击")
# 可以添加额外的操作，比如点击按钮等

# 关闭浏览器
driver.quit()