---
layout: post
title: Python quick tutorial
date: 2016-10-06 11:03:32 +0800
categories: language python
---

This is the personal python tutorial for quick reference.
If you read this article by chance, you better skip or ignore it.
It won't fit you, because it's just a collections of some pieces of my notes when I learning python.

#### Get help
```python
import this
# then read the output sentences carefully
import os
>>> dir(os)
>>> help(os.chown)
>>> print(os.__doc__)
```

#### Four kind of most important data type, String, List, Tuple, Dictionary
variables in python are not necessary to be declared, assign a value before use it,
at the same time, you cannot refer to a variable you did not assign

##### String
```python
s = 'Hello'
```

- immutable
- double quote or single quote, no big difference between them, but single quote is more common in python
- use the syntax s[m:n] to refer the element start from m to n (not including n)
- add the prefix 'r' to create a raw string, which can disable the interpretation of special character

##### List
```python
l = [1, 2, 3]
```

- mutable
- bracket
- use 'for' to iterate a list

```python
>>> for i in l:
...     print i
```
- check the existing of a element in a list

```python
>>> if 1 in l:
...     print '1 is one element of l'
```
- conversion between list and string, `s.join` and `l.split`

##### Tuple
```python
t = (1, 2, 4, 3)
```

- immutable
- parenthesis
- other operations are very similar with list, but more efficient
- a cool feature of tuple, assign value to multiple variable at the same time, `(x, y) = (1, 3)`
- c style formatted output, `'x = %d, y = %d' % (2, 3)`

##### Dictionary
```python
d = {}
d['a'] = 'alpha'
d['o'] = 'omega'
d['e'] = 'gamma'
```

- a combination of keys and values, think it as map, hashmap, etc.
- `d['x']` will raise `KeyError`, but `d.get('x')` just return `None`
- check the existence of a key, `'x' in d`
- `d.keys()` and `d.values()` will return a list of keys and a list of values respectively
- `d.items()` will return key-value pair as a list of tuple

#### File operations

##### read from file

```python
>>> f = open('/etc/passwd', 'rU')
>>> for line in f:
...     print line
```

##### write to a file

```python
>>> f = open('/home/mutter/test.txt', 'w+')
>>> f.write('a python generated string')
>>> f.flush()
>>> f.close()
```

#### Regular expression
```python
import re
match = re.search(pattern, text)
if match:
    match.group()

re.findall(pattern, text)
# return a matched list
```
if pattern has group separator, we can use `match.group(1), match.group(2), ...` to refer the results.

#### interaction between os and other utils
```python
import os
import sys
import shutil
import commands
```
when import a module, python interpreter will evaluate the entire module file from beginning to end.

#### Exception handling
```python
>>> try:
...     d['x']
... except KeyError:
...     print 'key error'
... finally:
...     print 'I\'m finally'
... 
```

#### HTTP request
```python
import urllib
uf = urllib.urlopen('http://cn.bing.com')
uf.read()
urllib.urlretrieve('http://cn.bing.com', 'bing.html')
```
