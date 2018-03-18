---
layout: post
title: A Simple Approach to Convert One Character from GBK to utf8
date: 2018-03-18 07:21:59 +0000
categories: java
---

From [wikipedia](!https://en.wikipedia.org/wiki/GBK_(character_encoding)) article we know that a GBK encoding character include one or two bytes. If the first character is within the range `0x00~0x7f`, it presents a character in ascii encoding table, we can convert it to ascii and do whatever we want to the converted character.

Otherwise, the first character is not within the bound `0x00~0x7f`, which means it has the most significant bit set, then the first character and the second character together denote a GBK encoding character. We can construct a valid and completed GBK encoding character and do whatever we want to this character from these two bytes.

To show how it works, follow the steps below.

1. obtain a GBK encoding file
   
   I use the below command to create an GBK encoding file
   ```sh
   $ vim myfile-utf8
   # type anything GBK character
   # quit vim
   $ iconv -f utf8 -t gbk myfile-utf8 > myfile-gbk
   ```
   
2. Now we can use the simple rule described above to parse the GBK encoding file

   ```kotlin
   fun main(args: Array<String>) {
   
       val inputStream = FileInputStream(File("/home/mutter/myfile-gbk"))
   
       val byteArray = ByteArray(inputStream.available()).apply { inputStream.read(this) }
   
       val iterator = byteArray.iterator()
   
       val stringBuilder = StringBuilder()
   
       while (true) {
           if (iterator.hasNext()) {
               val next = iterator.nextByte()
   
               // it's two bytes gbk encoding if the most significant bit(MSB) is 1
               if (next.and(0x80.toByte()) == 0x80.toByte()) {
                   if (iterator.hasNext()) {
                       val nn = iterator.nextByte()
                       val gbkString = String(byteArrayOf(next, nn),
                               Charset.forName("GBK"))
                       stringBuilder.append(gbkString)
                   } else {
                       break
                   }
               } else {
                   stringBuilder.append(String(byteArrayOf(next), Charsets.US_ASCII))
               }
           } else {
               break
           }
       }
       inputStream.close()
   
       println(stringBuilder.toString())
   }
   ```
