这是一个Sublime Text 3 插件。    
如果你只想使用 python，可以只看 test.py

因工作原因，需要从邮件中手机一些收件地址，给他们寄出快递。    
由于特殊情况，不能要求对方们使用填写表单的方式收集。    
需整理的数量有点多，而且他们发来的格式乱七八糟，要整理成方便寄件的文字格式，怎么办？  
  
<br>

理想中的文本格式：  

```
姓名   手机        地址
------------------------------------------------------
周树人 15200000000 北京市西城区阜成门内宫门口二条19号
```

<br>  

实际发来的：  

```
地址：北京市西城区阜成门内宫门口二条19号
电话：152-0000-0000
姓名：周树人
```


```
15200000000，北京市西城区阜成门内宫门口二条19号，周树人（收）
```


```
北京市西城区阜成门内宫门口二条19号
15200000000 
周树人
```


```
收货人: 周树人
手机号码: 15200000000
所在地区: 北京市西城区
详细地址: 阜成门内宫门口二条19号
```

<br>

反正各种各样的都有，要不就包含其他的分隔符号，或者不加空格啊，加了一边另一边不加啊。。总之看着就头疼。  
从QQ邮箱复制的时候，还可能顺便复制到地址或手机号的浮动提示文字。  


因为平时都在用SublimeText 作为文本编辑器。  
所以把它做成 Sublime Text 3 的插件，会更加方便 (感谢 @hyrious 技术支持！)

<br>

## 如何安装

在 [Packages] 新建一个 [SplitReverse] 文件夹，里面放入这里的6个文件。

> **如何找到[Packages]**： Sublime Text 上方的菜单：[Preferences - Browse Packages...]

```
└─SplitReverse
    ├─SplitReverse.py
    ├─SplitReverse.sublime-commands
    ├─Default (Windows).sublime-keymap
    ├─Default (Linux).sublime-keymap
    ├─Default (OSX).sublime-keymap
    └─Context.sublime-menu
```

<br>

### SplitReverse.py

```python
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

        # 正则匹配规则
        regex_phone   =  r'1\d{10}'
        regex_phone2  =  r'(\d{3})(-)?(\d{4})(-)?(\d{4})'
        regex_address =  r'([^(\d|\s)$省]+省|.+自治区)?([^市]+市)([^县]+县|.+区)?(.*)'
        regex_split   =  r'(\n)|(\+)|(\\)|(\.)|(\~)|(，)|(。)|(,)|(;)|(？)|(：)|(:)|(\?)'
        regex_delete  =  r'(收件地址)|(收货地址)|(所在地区)|(详细地址)|(联系号码)|(手机号码)|(联系电话)|(手机号)|(收货人)|(收件人)|(（收）)|(号码)|(手机)|(名字)|(地址)|(电话)|(姓名)|(可能是电话号码，是否拨号?)|(在地图中查看)'

        # 分隔换行符
        split_line = re.sub(regex_split ,' ', text.strip().lstrip().rstrip()).split()

        # print(split_line)

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
```

<br>

### Context.sublime-menu
让插件显示在右键菜单中

```json
[
    {
        "id": "split_reverse",
        "command": "split_reverse",
        "caption": "SplitReverse"
    }
]
```

<br>

### Default (Windows).sublime-keymap
让插件支持快捷键。这里Windows / Linux 的快捷键是一样的

```json
[
    {
        "keys": ["ctrl+alt+a"], 
        "command": "split_reverse" 
    }
]
```

<br>

### Default (OSX).sublime-keymap
Mac 的快捷键

```json
[
    {
        "keys": ["command+shift+a"], 
        "command": "split_reverse" 
    }
]
```

<br>

## 如何使用

我习惯将一段文本粘贴进去，按 Ctrl + A全选，然后 Ctrl + Alt + A 执行。

<br>


## 常见问题

> 1. 如果[地址][名字]之间没有空格作为分隔，需先手动加一个空格分隔，再执行脚本。  
> 2. 如果[手机号]中使用特殊符号作为分隔，需先手动删除特殊符号(选中一个之后按 Ctrl + D，可快速选择更多)  
> 3. 如果[地址]中包含了空格分隔，可能会变成[名字]，所以需要先手动调整。  

<br>

## 特别感谢

@hyrious 提供的技术支持！

<br><br>
