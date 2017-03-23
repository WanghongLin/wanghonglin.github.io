---
layout: post
title: Build libpng for Android
date: 2017-03-20 09:08:02 +0800
categories: android
---

### Get the source

```sh
$ mkdir $HOME/libpng-android
$ cd ~/libpng-android
$ wget https://nchc.dl.sourceforge.net/project/libpng/libpng16/1.6.29/libpng-1.6.29.tar.xz
$ wget http://zlib.net/zlib-1.2.11.tar.gz
```

### Extract the source and prepare `Android.mk`, `Application.mk`

```sh
$ mkdir jni && cd jni
$ tar Jxvf ../libpng-1.6.29.tar.xz
$ tar zxvf ../zlib-1.2.11.tar.gz
```

With the help of [this](https://github.com/WanghongLin/generate-android-mk/blob/master/generate_android_mk.py) python script to create `Android.mk`


* Create `Android.mk` for `libpng`, `jni/libpng-1.6.29/Android.mk`

```makefile
# Auto-generated module by script
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

LOCAL_MODULE := libpng
LOCAL_C_INCLUDES := 
LOCAL_CFLAGS :=
LOCAL_CPPFLAGS := 
LOCAL_LDLIBS := 
LOCAL_SHARED_LIBRARIES := 
LOCAL_STATIC_LIBRARIES := libz
LOCAL_PREBUILTS := 
LOCAL_SRC_FILES := ./png.c \
./pngerror.c \
./pngget.c \
./pngmem.c \
./pngpread.c \
./pngread.c \
./pngrio.c \
./pngrtran.c \
./pngrutil.c \
./pngset.c \
./pngtrans.c \
./pngwio.c \
./pngwrite.c \
./pngwtran.c \
./pngwutil.c \
./arm/arm_init.c \
./arm/filter_neon.S \
./arm/filter_neon_intrinsics.c


include $(BUILD_STATIC_LIBRARY)

# Auto-generated module by script
include $(CLEAR_VARS)

LOCAL_MODULE := pngtest
LOCAL_C_INCLUDES := 
LOCAL_CFLAGS := 
LOCAL_CPPFLAGS := 
LOCAL_LDLIBS := 
LOCAL_SHARED_LIBRARIES := 
LOCAL_STATIC_LIBRARIES := libpng
LOCAL_PREBUILTS := 
LOCAL_SRC_FILES := ./pngtest.c

include $(BUILD_EXECUTABLE)
```

* Create `jni/zlib-1.2.11/Android.mk`

```makefile
# Auto-generated module by script
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

LOCAL_MODULE := libz
LOCAL_C_INCLUDES := 
LOCAL_CFLAGS := 
LOCAL_CPPFLAGS := 
LOCAL_LDLIBS := 
LOCAL_SHARED_LIBRARIES := 
LOCAL_STATIC_LIBRARIES := 
LOCAL_PREBUILTS := 
LOCAL_SRC_FILES := ./adler32.c \
./compress.c \
./crc32.c \
./deflate.c \
./gzclose.c \
./gzlib.c \
./gzread.c \
./gzwrite.c \
./infback.c \
./inffast.c \
./inflate.c \
./inftrees.c \
./trees.c \
./uncompr.c \
./zutil.c \

include $(BUILD_STATIC_LIBRARY)
```

* And the top level script `jni/Android.mk`, `jni/Application.mk`

```makefile
# top level Android.mk
include $(all-subdir-makefiles)
```

```makefile
# top level Application.mk, PIE flag to run test program
APP_PLATFORM := android-16
```

### Other preparation for correctly build

We need to create `pnglibconf.h` for `libpng` build

```sh
$ cd ~/libpng-android/jni/libpng-1.6.29/
$ make -f scripts/pnglibconf.mak
```

Also, for `libpng` build, tell it to ignore zlib version checking.

Comment the error preprocessing line.

```c
// #  error ZLIB_VERNUM != PNG_ZLIB_VERNUM \
    ......
```

### Invoke the build and test the result

```sh
$ cd ~/libpng-android
$ ndk-build
# after the build done
$ adb push libs/armeabi-v7a/pngtest /data/local/tmp/
$ adb push jni/libpng-1.6.29/pngtest.png /data/local/tmp/
# go to your device shell and run the test
$ adb shell
$ cd /data/local/tmp/
$ ./pngtest
```

All steps above are bundled together in a single script, and can be found [here](https://raw.githubusercontent.com/WanghongLin/compile-scripts/master/compile-libpng-android.sh).
