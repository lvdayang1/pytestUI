import pyautogui as pyautogui
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
import time
from PIL import Image
from pytesseract import pytesseract

"""封装selenium基本操作"""


class LocatorTypeError(Exception):
    pass


class ElementNotFound(Exception):
    pass


class Base():
    """基于原生的selenium做二次封装"""

    def __init__(self, driver:webdriver.Chrome, base_url='',  timeout=10, t=0.5):
        self.driver = driver
        self.timeout = timeout
        self.t = t
        self.base_url = base_url

    def open(self, url):
        '''跟get方法一样'''
        self.driver.get(url)
        #self.driver.get(self.base_url + url)

    def maxBroswer(self):
        # 浏览器最大化
        self.driver.maximize_window()

    def windowSize(self,l,r):
        self.driver.set_window_size(l,r)

    def closeBrowser(self):
        # 关闭当前界面
        self.driver.close()

    def quitBrowser(self):
        # 关闭浏览器
        self.driver.quit()

    def fresh(self):
        # 刷新界面
        self.driver.refresh()

    def back(self):
        # 浏览器后退按钮
        self.driver.back()

    def forward(self):
        # 浏览器前进按钮
        self.driver.forward()

    def find(self, locator):
        """locator必须是元祖类型：loc = ('id','value1') 定位到元素，返回元素对象，没定位到，Timeout异常"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        else:
            print("正在定位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            try:
                ele = WebDriverWait(self.driver, self.timeout, self.t).until(EC.presence_of_element_located(locator))
            except TimeoutException as msg:
                raise ElementNotFound("定位元素出现超时！！！！"
                                      "先把定位技术学好，别复制粘贴xpath, 请检查你的定位方式，在浏览器先调试成功，观察页面是否正常打开")
            return ele

    def finds(self, locator):
        '''复数定位，返回elements对象 list  '''
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        else:
            print("正在定位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            eles = WebDriverWait(self.driver, self.timeout, self.t).until(EC.presence_of_all_elements_located(locator))
            return eles

    def send(self, locator, text=''):
        '''发送文本'''
        ele = self.find(locator)
        if ele.is_displayed():
            ele.send_keys(text)
        else:
            raise ElementNotVisibleException("元素不可见或者不唯一无法输入，解决办法：定位唯一元素，或先让元素可见，或者用js输入")

    def click(self, locator):
        '''点击元素'''
        ele = self.find(locator)
        if ele.is_displayed():
            ele.click()
        else:
            raise ElementNotVisibleException("元素不可见或者不唯一无法点击，解决办法：定位唯一元素，或先让元素可见，或者用js点击")

    def clear(self, locator):
        '''清空输入框文本'''
        ele = self.find(locator)
        ele.clear()

    def is_selected(self, locator):
        """判断元素是否被选中，返回bool值"""
        ele = self.find(locator)
        r = ele.is_selected()
        return r

    def is_element_exist(self, locator):
        try:
            self.find(locator)
            return True
        except:
            return False

    def is_title(self, title=''):
        """返回bool值"""
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_is(title))
            return result
        except:
            return False

    def is_title_contains(self, title=''):
        """返回bool值"""
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_contains(title))
            return result
        except:
            return False

    def is_text_in_element(self, locator, text=''):
        """返回bool值"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.text_to_be_present_in_element(locator, text))
            return result
        except:
            return False

    def is_value_in_element(self, locator, value=''):
        """返回bool值，value为空字符串，返回False"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.text_to_be_present_in_element_value(locator, value))
            return result
        except:
            return False

    def is_alert(self, timeout=3):
        '''判断alert是否存在，存在返回alert对象'''
        try:
            result = WebDriverWait(self.driver, timeout, self.t).until(EC.alert_is_present())
            return result
        except:
            return False

    def get_title(self):
        """获取title"""
        return self.driver.title

    def get_text(self, locator):
        """获取文本"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        try:
            t = self.find(locator).text
            return t
        except:
            print("获取text失败，返回''")
            return ""

    def get_attribute(self, locator, name):
        """获取属性"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        try:
            element = self.find(locator)
            return element.get_attribute(name)
        except:
            print("获取%s属性失败，返回''"%name)
            return ''

    def js_focus_element(self, locator):
        """聚焦元素"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        target = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def js_scroll_top(self):
        """滚动到顶部"""
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self, x=0):
        """滚动到底部"""
        js = "window.scrollTo(%s, document.body.scrollHeight)"%x
        self.driver.execute_script(js)

    def select_by_index(self, locator, index=0):
        """通过索引，index是索引第几个，从0开始，默认第一个"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        element = self.find(locator)
        Select(element).select_by_index(index)

    def select_by_value(self, locator, value):
        """通过value属性"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        element = self.find(locator)
        Select(element).select_by_value(value)

    def select_by_text(self, locator, text):
        """通过文本值定位"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        element = self.find(locator)
        Select(element).select_by_visible_text(text)

    def select_object(self, locator):
        '''返回select对象'''
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        element = self.find(locator)
        return Select(element)

    '''获取下拉选择器的所有属性'''
    def get_selector_all_options(self, locator):
        option = []
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        selector = Select(self.find(locator))
        options = selector.options
        for index in range(0, len(options) - 1):
            option.append(options[index])
            #print(options[index])
        return option

    '''获取下拉选择器的所有值'''
    def get_selector_all_options_value(self, locator):
        option_value = []
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        selector = Select(self.find(locator))
        options = selector.options
        for index in range(0, len(options) - 1):
            option_value.append(options[index].text)
            # print(options[index].text)
        return option_value

    def switch_iframe(self, id_index_locator):
        """切换iframe"""
        try:
            if isinstance(id_index_locator, int):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, str):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, tuple):
                ele = self.find(id_index_locator)
                self.driver.switch_to.frame(ele)
        except:
            print("iframe切换异常")

    '''返回切入frame之前的窗体'''
    def default_content(self):
        self.driver.switch_to.default_content()

    ''' 获取当前窗口句柄'''
    def current_handle(self):
        return self.driver.current_window_handle

    '''切换至指定窗口'''
    def switch_handle(self, window_name):
        self.driver.switch_to.window(window_name)

    ''' 切换窗口，两窗口适用'''
    def switch_to_handle(self):
        time.sleep(3)
        handles = self.driver.window_handles  # 获取当前窗口句柄集合（列表类型）
        for handle in handles:
            if handle == self.driver.current_window_handle:
                self.driver.switch_to.window(handles[-1])

    '''有的审核操作弹出新页面，然后审核通过后页面关闭，判断审核完成可用这个，类似于untilTime，等待加载完成'''
    def handle_only(self):
        while 1:
            if len(self.driver.window_handles) == 1:
                break

    def switch_alert(self):
        r = self.is_alert()
        if not r:
            print("alert不存在")
            return ""
        else:
            return r

    def get_alert_text_accept(self):
        '''获取alert文本值, 并点确定'''
        alert = self.is_alert()
        if alert:
            text = alert.text
            print("获取到alert内容：", text)
            # 点确定按钮
            alert.accept()
            print("点alert确定按钮")
        else:
            text = ""
            print("没有获取到alert内容：")
        return text

    def get_alert_text_dismiss(self):
        '''获取alert文本值, 并点确定'''
        alert = self.is_alert()
        if alert:
            text = alert.text
            print("获取到alert内容：", text)
            # 点确定按钮
            alert.dismiss()
            print("点alert取消按钮")
        else:
            text = ""
            print("没有获取到alert内容：")
        return text

    def move_to_element(self, locator):
        """鼠标悬停操作"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        ele = self.find(locator)
        ActionChains(self.driver).move_to_element(ele).perform()

    def mouse_double_click(self, locator):
        """双击鼠标左键"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        ele = self.find(locator)
        ActionChains(self.driver).double_click(ele).perform()

    """右击操作locator：元素的属性名（ID等）和属性值"""
    def mouse_context_click(self,locator):
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        ele = self.find(locator)
        ActionChains(self.driver).context_click(ele).perform()

    """右键后操作右键内容（只有GUI时才可用），list操作的序列 ['down', 'down', 'down', 'down',  'enter', 'enter']"""
    def typewrite(self,list):
        pyautogui.typewrite(list)

    def screenshot(self, path):
        """ path = "D:\baidu_img.jpg """
        """ 截图 """
        self.driver.get_screenshot_as_file(path)

    """鼠标拖放操作"""
    """能定位到目标拖放位置时使用"""
    def drag_and_drop(self,locator1,locator2):
        if not isinstance(locator1, tuple):
            raise LocatorTypeError("参数类型错误，locator1必须是元祖类型：loc = ('id','value1')")
        if not isinstance(locator2, tuple):
            raise LocatorTypeError("参数类型错误，locator2必须是元祖类型：loc = ('id','value1')")
        elem = self.find(locator1)
        tar = self.find(locator2)
        ActionChains(self.driver).drag_and_drop(elem, tar).perform()

    '''鼠标拖放，不能定位目标位置时使用，这种方式可以使用目标位置的相对位置'''
    '''locator:滑块元素的属性名和属性值'''
    '''x,y 目标位置的相对坐标'''
    def move(self, locator,x, y):
        # 获取拖拽的圆球
        if not isinstance(locator, tuple):
            raise LocatorTypeError("参数类型错误，locator必须是元祖类型：loc = ('id','value1')")
        slideblock = self.find(locator)
        # 鼠标点击圆球不松开
        ActionChains(self.driver).click_and_hold(slideblock).perform()
        # 将圆球滑至相对起点位置的最右边
        ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=y).perform()

    '''获取table所有行attrib:table标签的属性（ID，XPATH，CLASS_NAME等） attrCont：table属性值'''
    '''获取的所有行包括表头，为一个列表，列表下标从0开始'''
    def table_rows(self, locator):
        table = self.find(locator)
        return table.find_elements_by_tag_name("tr")

    '''获取table表头  table_rows：为table的所有行,ele:为table第一行的标签属性，th或td'''
    '''获取的所有列为一个列表，列表下标从0开始'''
    def table_cels(self, table_rows, ele):
        return table_rows[0].find_elements_by_tag_name(ele)

    '''获取验证码，返回的是验证码里的字符串'''
    '''locator：图片的属性名（ID等）和属性值'''
    '''使用方法'''
    #         while 1:
    #             driver.find_element_by_id("username").send_keys("kjjrcxq")
    #             ele = driver.find_element_by_id("sec_code")
    #             ele.send_keys("111111")
    #           #  调用获取验证码方法
    #             vcode = self.basecommon.verification_code("ID","img_checkcode")
    #           #  输入验证码
    #             driver.find_element_by_id("checkcode").send_keys(vcode)
    #           #  点击提交
    #             driver.find_element_by_id("submit").click()
    #           # 通过判断是否到下一步，判断验证码是否输入正确
    #             if self.driver.current_url == r"http://test.gzkcw.egrant.cn/egrantweb/select-user-role":
    #                 break
    def verification_code(self, locator):
        # 获取全屏图片，并截取验证码图片的位置
        self.driver.get_screenshot_as_file('verification_code_image.png')
        location = self.find(locator).location
        size = self.find(locator).size
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        a = Image.open("verification_code_image.png")
        im = a.crop((left, top, right, bottom))
        im.save('verification_code_image.png')
        time.sleep(1)
        # 打开保存的验证码图片
        image = Image.open("verification_code_image.png")
        # 图片转换成字符
        vcode = pytesseract.image_to_string(image)
        #print(vcode)
        return vcode


if __name__ == "__main__":
    driver = webdriver.Chrome()
    web = Base(driver)  # 实例化
    driver.get("https://www.baidu.com")
    loc_1 = ("id", "kw")
    web.send(loc_1, "hello")

    # Python is likely shutting down
    driver.close()