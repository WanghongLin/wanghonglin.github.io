---
layout: post
title: Java Naming Rules
date: 2017-06-01 22:51:01 +0800
categories: android
---

此文大量参考了《代码大全2》的第11章，《变量名的力量》，里面总结了大量实用的软件工程实践方法，适合任何阶段的程序员阅读。初出茅庐的菜鸟可以从中发现许多有益的编程技巧，经验丰富的大牛可以从中获得许多软件工艺之道。

此文针对使用Android studio进行Android应用开发的部分建议规范，其他IDE或者编程语言可以忽略此文。

#### 一般规则

* 完全、准确描述变量代表的事物

请使用 `personTotal, velocity, currentDate`

勿使用 <del>`written, ct, x1, x2`</del>

* 好名字应该表达是“什么”（what），而不是“如何”（how）

对于应用层编码，通常涉及到一些产品逻辑以及业务逻辑，同时还会大量操纵实现中的实体，好名字应该尽量描述事物及问题，而不是计算机内部的实现和处理。

请使用 `employeeData, printerReady, sum`

勿使用 <del>`inputRec, bitFlag, calcVal`</del>

* 名字的长度在10～16个字符之间

* 把计算结果限定词加到名字的后面，突出前面名次的主要含义，保持一致性

常用的计算结果限定词`Total, Sum, Average, Max, Min, Record, String, Pointer`

请使用 `personTotal, urlString, scoreAverage`

勿使用 <del>`totalPerson, stringUrl, averageScore`</del>

* 使用约定俗成的对仗词语

```
begin/end, first/last, locked/unlocked, min/max, next/previous, up/down

old/new, opened/closed, visible/invisible, source/target, source/destination
```

#### 命名细节

* 方法（method）以及成员（field）、变量名都必须使用`camelCase`的写法

对于成员（field），Android框架里面的代码里面含有大量的以`m`为前缀的命名，`mContext, mStarted, mMuxer`。

这种命名在Android Studio当中使用极其不方便，smart变量名自动提示不会自动加上`m`前缀，自动生成的`set/get`方法还需要再次修改，所以应该避免使用这种带前缀`m`的命名方式

* 常量必须使用大写，并且使用下划线（underscore）`_` 进行分隔

比如 `ALL_CAPS`，在Android studio当中使用`const` Live Template 快速创建针对 Android 的常量

* 循环下标的命名

1. 通用的循环下标，使用 i/j/k
2. 用来操作图形／像素的下标 x/y/z
3. 用其他更好的名字 `teamIndex, pictureIndex, employeeIndex`

* 绝对不允许用flag表示状态变量

加更多的前缀和后缀使人一眼就可以看出该状态变量的含义和意图

* 布尔变量命名

使用简单的命名 `done, error, found, success, ok`，或者使用更加具有含义的命名 `frameAvailable, fileExists, sourceFileFound`

* 使用前缀约定枚举类型／相互关联的常量

```java
public enum Color {
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE
    //...
}

public static final int IO_SUCCESS = 0x01
public static final int IO_ERROR_UKNOWN = 0x02;
public static final int IO_ERROR_INSUFFICIENT_STORAGE = 0x04;
public static final int IO_ERROR_DEVICE_NOT_AVAILABLE = 0x08;
```

#### 当你实在想不到好的名字的时候

使用Android Studio的变量名智能自动提示 `Control + space`/`Control + Shift + space`

使用IDE内部自带的规范总比每一个人天马行空来一个名字要具有更好的可读性
