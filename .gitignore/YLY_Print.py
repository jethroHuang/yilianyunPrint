"""
易联云1.4.0文档   http://doc.10ss.net
排版指令
    字体加大 <FS>str</FS>
    字体加粗 <FB>str</FB>
    字体加高 <FH>str</FH>
    字体加宽 <FW>str</FW>
    换行 \r \n \r\n
    居中对齐 <center>str</center>
    右对齐 <right>str</right>
    一行三格或四格对齐排版 <table><tr><td>列1</td><td>列2</td><td>列3</td></tr></table>
        <table></table>:  表示排版
        <tr></tr>:  表示行，一个table可以有多行
        <td></td>:  表示列，每行有且只有三个列或四个列
        注意:  该标签中不允许出现换行符和其它标签符号，否则无法准确排版
    制表符 \t  四字符对齐打印
"""

def get_QR(text):
    """
    获取二维码指令
    :param text: str为二维码内容，内容不超过96个字符
    :return: 二维码打印指令
    """
    if len(text) > 96:
        return "<QR>内容超过96个文字,打印失败</QR>"
    else:
        return "<QR>" + text + "</QR>"


def get_BR(text):
    """
    获取条形码指令
    :param text:条形码内容，13位数字(中文或其他字符无效，数据不足13位自动补0，补齐13位,超出13位裁取前13位)
    :return: 条形码打印指令
    """
    if text.isdigit():
        if len(text) > 13:
            text = text[:13]
        return "<BR>{}</BR>".format(text)
    else:
        return "字符串内容必须为全数字"


class YLY_Print:
    import requests
    import hashlib
    import time
    import json

    def __init__(self, partner, api_key, username):
        """
        初始化对象
        :param partner:  用户 id
        :param api_key:  API 密钥
        :param username  用户名
        API 密钥获取地址(系统集成) http://yilianyun.10ss.net/apisystem/apisystem
        """
        self.partner = partner
        self.api_key = api_key
        self.username = username

    def sign_md5(self, sign):
        return self.hashlib.md5(sign.encode("utf-8")).hexdigest().upper()

    def print(self, machine_code, machine_secret_key, content, repeat=0):
        """
        使指定打印机打印文本内容
        :param repeat: 多联打印,即重复打印多少次,取值范围1~9 包含1和9
        :param machine_code: 打印机终端号
        :param machine_secret_key: 打印机终端密钥
        :param content: 待打印的内容
        :return: 返回一个 dict 包含 state id
        文档 http://doc.10ss.net/578103?hkrgpk=dv9yi1
        """
        time_now = str(int(self.time.time()))  # 当前时间戳
        sign = self.api_key + 'machine_code' + machine_code + 'partner' + \
               self.partner + 'time' + time_now + machine_secret_key

        sign = self.sign_md5(sign)
        if 0 < repeat < 10:
            content = "<MN>{}</MN>".format(repeat) + content
        data = {"partner": self.partner,
                "machine_code": machine_code,
                "content": content,
                "time": time_now,
                "sign": sign
                }
        r = self.requests.post("http://open.10ss.net:8888", data=data)
        return r.json()

    def add_machine(self, machine_code, machine_secret_key, print_name, mobile_phone=""):
        """
        添加打印机
        :param machine_code: 打印机终端号
        :param machine_secret_key: 打印机终端密钥
        :param mobile_phone: 打印机上的手机号(方便充值话费) 可为空
        :param print_name: 打印机昵称
        :return: 状态码	说明
                    1	添加成功
                    2	重复
                    3	添加失败
                    4   添加失败
                    5	用户验证失败
                    6	非法终端号
        """
        sign = "machine_code" + machine_code + "mobilephone" + mobile_phone + \
               "partner" + self.partner + "printname" + print_name + "username" + self.username
        sign = self.sign_md5(self.api_key + sign + machine_secret_key)

        data = {
            "machine_code": machine_code,
            "partner": self.partner,
            "mobilephone": mobile_phone,
            "printname": print_name,
            "username": self.username,
            "sign": sign,
            "msign": machine_secret_key
        }

        r = self.requests.post("http://open.10ss.net:8888/addprint.php", data=data)
        return r.text

    def remove_machine(self, machine_code, machine_secret_key):
        """
        删除终端
        :param machine_code: 终端号
        :param machine_secret_key: 终端密钥
        :return:  状态码	说明
                    1	删除成功
                    3	删除失败
                    4   删除失败
                    5	用户验证失败
                    6	非法终端号
        """
        sign = self.api_key + "machine_code" + machine_code + "partner" + self.partner + machine_secret_key
        sign = self.sign_md5(sign)
        data = {
            "partner": self.partner,
            "machine_code": machine_code,
            "sign": sign
        }

        r = self.requests.post("http://open.10ss.net:8888/removeprint.php", data=data)
        return r.text
