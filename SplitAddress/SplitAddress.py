import sublime
import sublime_plugin
import re

class SplitAddressCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # 选中文本
        sel = self.view.sel()[0]

        # 忽略内容为空的情况
        if sel.empty(): 
            return

        # 提取选中的文本
        text = self.view.substr(sel)
 
        # 临时变量
        str_name, str_phone, str_address = '', '', ''

        # 正则匹配规则
        regex_phone   =  r'1\d{10}'
        regex_phone2  =  r'(\d{3})(-)?(\d{4})(-)?(\d{4})'
        regex_address =  r'([^(\d|\s)$省]+省|.+自治区)?([^市]+市)([^县]+县|.+区)?(.*)'
        regex_split   =  r'(\n)|(\+)|(\\)|(\.)|(\~)|(，)|(。)|(,)|(;)|(？)|(：)|(:)|(\?)'
        regex_delete  =  r'(收件地址)|(收货地址)|(所在地区)|(详细地址)|(联系号码)|(手机号码)|(联系电话)|(手机号)|(收货人)|(收件人)|(（收）)|(号码)|(手机)|(名字)|(地址)|(电话)|(姓名)|(可能是电话号码，是否拨号?)|(在地图中查看)'

        # 分隔换行符
        split_line = re.sub(regex_split ,' ', text.strip().lstrip().rstrip()).split()

        # 提取信息
        for s in split_line: 
            s = s.replace(' ', '')
            if s == '': continue;
            elif re.findall(regex_phone , s):  str_phone = str_phone + s;
            elif re.findall(regex_phone2 , s): s = s.replace('-' , ''); str_phone = str_phone + s;
            elif re.findall(regex_address, s): str_address = str_address + s;
            else: str_name = str_name +s;

        # 组合信息
        str_text = ' '.join([str_name, str_phone, str_address])
        str_text = re.sub(regex_delete ,'', str_text)

        # 替换文本
        self.view.replace(edit, sel, str_text)
