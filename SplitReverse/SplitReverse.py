import sublime
import sublime_plugin
import re

class SplitReverseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # 选中文本
        sel = self.view.sel()[0]
        if sel.empty(): return
        text = self.view.substr(sel)
 
        # 临时变量
        str_name, str_phone, str_address = '', '', ''

        #去除多余字符
        text = text.strip().lstrip().rstrip().replace('\n', ' ')
        regex  = r"(\+)|(\\)|(\.)|(\~)|(，)|(。)|(,)|(;)|(：)|(:)|(？)|(收件地址)|(收货地址)|(所在地区)|(详细地址)|(联系号码)|(手机号码)|(联系电话)|(手机号)|(收货人)|(收件人)|(（收）)|(号码)|(手机)|(名字)|(地址)|(电话)|(姓名)|(可能是电话号码，是否拨号?)|(在地图中查看)|(\?)"
        text = re.sub(regex ,' ',text) 

        # 分隔空格
        group = text.split()

        print(group)

        # 提取信息
        for s in group:
            if s == '': continue
            elif re.findall(r"(.*?)(省|自治区|市)|(.*?)(区|县|州)|(.*?)(街道|大道|巷|路口)|(.*?)(大厦|小区|工作室|公园|花园|公司|公寓|宿舍|驿站|学府|超市|旅馆|百货|便利店|大学)|(.*?)(室|座|号|楼|栋|单元)", s):  str_address = str_address + s
            elif re.findall(r'1\d{10}', s): str_phone = str_phone + s
            else: str_name = str_name +s
        
        # 组合信息
        str_text = ' '.join([str_name, str_phone, str_address])

        # 替换文本
        self.view.replace(edit, sel, str_text)
