import re

text = ("地址：北京市西城区阜成门内宫门口二条19号\n"
    "电话：15200000000\n"
    "姓名：周树人")

# 临时变量
str_name, str_phone, str_address = '', '', ''

#去除多余字符
regex  = r"(-)|(\+)|(，)|(,)|(;)|(地址：)|(收件地址：)|(收货地址：)|(所在地区: )|(详细地址: )|(手机号码: )|(收货人:)|(电话：)|(姓名：)|(（收）)|(可能是电话号码，是否拨号?)|(在地图中查看)"
text = re.sub(regex,' ',text) 
text = text.strip().lstrip().rstrip().replace('\n', ' ')

# 分隔空格
group = list(set(text.split()))

# 提取信息
for s in group:
    if s == '': continue
    elif re.findall(r"(.*?)(省|自治区|市)|(.*?)(区|县|州)|(.*?)(村|镇|街道)|(.*?)(座|号|楼|栋)", s):  str_address = str_address + s
    elif re.findall(r'1\d{10}', s): str_phone = str_phone + s
    else: str_name = str_name +s

# 组合信息
str_text = ' '.join([str_name, str_phone, str_address])

# 输出结果
print(str_text)
