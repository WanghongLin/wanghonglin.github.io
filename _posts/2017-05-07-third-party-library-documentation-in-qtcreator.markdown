---
layout: post
title: Third-party library documentation in QtCreator
date: 2017-05-07 03:15:16 +0000
categories: qt
---

对比其他的IDE，QtCreator在Linux是一个不错的选择，对于C/C++开发，具有自动补齐/语法高亮/CMake支持等重要的功能。

美中不足的就是，对于外部的第三方库，QtCreator的文档支持不是很好，需要对其修正一些东西，才可以比较方便地使用。

在QtCreator当中，查看文档有两种方式。

1. hover documentation/tooltips，只要把鼠标放到函数调用或者类名字上面，就会弹出一段简短描述
2. 在上面的基础上，使用`F1`可以打开更加详细的qthelp HTML文档，以下用`F1帮助文档`来代替

下面以`FFmpeg`为例，简要描述如何在QtCreator当中添加第三方库的文档支持

### F1帮助文档

QtCreator的`F1帮助文档`可以方便地从`Doxygen`当中构建，如果你使用的第三方项目已经有`Doxygen`文档支持了，可以在`Doxygen`的
配置文件当中修改（添加）以下的参数生成在QtCreator当中可以直接使用的`F1帮助文档`

```
GENERATE_QHP           = YES
QCH_FILE               = FFmpeg.qch
QHP_NAMESPACE          = org.ffmpeg.Project
QHG_LOCATION           = /usr/bin/qhelpgenerator
```

以`FFmpeg`为例，通过执行`make apidoc`，然后在`Makefile`里面执行`Doxygen`就可以生成QtCreator可以识别的帮助文件

`doc/doxy/html/FFmpeg.qch`，全称是Qt Compressed Help，可以简单地看作是一些HTML文档的聚合

然后在QtCreator的设置里面添加进入

`Tools -> Options -> Documentation -> Add` 

此时，对于C++的项目应该就可以正常使用。

但是对于`FFmpeg`这个仅仅是提供C API的项目，还需要改一点东西才能找到函数调用的`F1帮助文档`，实现跳转。

上面提到的qch的文件是通过qhp（一个描述Qt Help Project的XML文件）使用`qhelpgenerator`生成的。

要在QtCreator当中显示一个符号的`F1帮助文档`，qhp文件里面必须有一个`<keyword>`的XML标签对应与之对应。

以`FFmpeg`的一个函数调用`avformat_open_input`为例，如下

```xml
<keyword name="avformat_open_input" id="lavf_decoding::avformat_open_input" ref="group__lavf__decoding.html#ga31d601155e9035d5b0e7efedc894ee49" />
```

QtCreator会根据`id`属性进行符号匹配，如果使用上面的qhp的关于`avformat_open_input`的描述，在QtCreator当中是无法找到该符号的帮助文档的。

因为是C API，在使用的时候，没有`lavf_decoding::`这个`namespace`，所以我们需要去掉这个前缀，在QtCreator当中才能找到这个符号的帮助。


### Hover documentation/Popup tooltips（中文不好怎么描述）

为了在tooltips里面显示简要的帮助文档，需要在HTML帮助文档里面加入QtCreator专用的标记。

1. 对于类名字的标记应该是下面的格式（我没有尝试）

```html
<!-- $$$className -brief A simple description of this class -->
<p> Only the first p tag will be displayed in QtCreator tooltips </p>
<p> .... </p>
<!-- @@@className -->
```

2. 对于函数名或者方法名，具有以下格式

```html
<!-- $$$function_name[overload1]$$$ -->
<p> Only the first p tag will be displayed in QtCreator tooltips </p>
<p> .... </p>
<!-- @@@function_name -->
```

在生成的HTML帮助文档里面添加以上的标记，就可以在QtCreator当中的tooltips里面显示类名或者函数调用的简要描述了。

### 对于没有使用Doxygen构建文档的项目

自己生成qhp文件，在qhp文件里面指定所需要的HTML文档，然后用`qhelpgenerator`生成QtCreator可以使用的qch文件。

1. qhp文件的描述可以参考这里，http://doc.qt.io/qt-4.8/qthelpproject.html
2. 有人从Linux manpages创建了QtCreator的帮助，参见这篇博文，http://shinnok.com/rants/2011/07/19/linux-man-pages-integration-with-qt-creator/
3. 这个项目使用脚本构建了OpenGL的QtCreator帮助文档，https://code.google.com/archive/p/qtcreator-openglhelp/


最后写了一个简单的[脚本](https://github.com/WanghongLin/miscellaneous/blob/master/tools/doxygen-c-api-qtcreator-fix.py)来处理上面描述的两种修改，修改qhp文件以及在HTML当中添加标记。

### 参考资料
1. 原来早有人有这个需求，http://lists.qt-project.org/pipermail/qt-creator/2015-January/004350.html
2. 关于QtCreator帮助文档使用特殊标记的参考，https://github.com/mmmarcos/doxygen2qtcreator/blob/master/doxygen2qtcreator.py
3. 另一个使用Doxygen的例子，http://blog.qt.io/blog/2014/08/13/qt-weekly-17-linking-qt-classes-in-documentation-generated-with-doxygen/
4. Qt的博客描述，http://blog.qt.io/blog/2008/06/20/introducing-doxygen2qthelp-create-qch-files-from-doxygen-finally/
5. 介绍Doxygen使用的文章，https://www.ibm.com/developerworks/aix/library/au-learningdoxygen/?S_TACT=105AGX52&S_CMP=content
6. [Qt Creator Documentation Gallery](https://wiki.qt.io/Qt_Creator_Documentation_Gallery) 上面可以直接下载一些帮助文档
