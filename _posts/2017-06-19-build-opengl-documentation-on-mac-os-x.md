---
layout: post
title: Build OpenGL documentation on Mac OS X
date: 2017-06-19 08:09:08 +0800
categories: misc
---
It's productive and helpful to use `man` to lookup `OpenGL` API from terminal. Basically this [guide](https://www.khronos.org/opengl/wiki/Getting_started/XML_Toolchain_and_Man_Pages) has covered everything how to build `OpenGL` documentation from scratch.

There are some little problems if we follow the guide in Mac OS X, and follows is my workarounds to make the build step run properly.

1. Using `svn` to checkout the man pages you want to build, like the guide said, e.g by run 
    ```shell
    $ svn co --username anonymous --password anonymous https://cvs.khronos.org/svn/repos/ogl/trunk/ecosystem/public/sdk/docs/man3/
    ```

2. Use `wget` to retrieve all the archives, don't forget to add the `-L` option if you use `curl`, `wget` will handle http redirect automatically for you, but not `curl`.

    ```shell
    $ wget http://www.docbook.org/xml/4.3/docbook-xml-4.3.zip
    $ wget http://www.w3.org/Math/DTD/mathml2.tgz
    $ wget http://www.docbook.org/xml/mathml/1.1CR1/dbmathml.dtd
    $ wget -O docbook-xsl-1.76.1.tar.bz2 https://sourceforge.net/projects/docbook/files/docbook-xsl/1.76.1/docbook-xsl-1.76.1.tar.bz2/download
    # then extract all of them
    ```

3. Change the url path in file `man3/xhtml/opengl-man.xsl` to a local path 
	```shell
	$ svn diff ../man3/xhtml/opengl-man.xsl  --force
	Index: ../man3/xhtml/opengl-man.xsl
	===================================================================
	--- ../man3/xhtml/opengl-man.xsl	(revision 33492)
	+++ ../man3/xhtml/opengl-man.xsl	(working copy)
	@@ -2,7 +2,7 @@
	 <xsl:stylesheet
	     xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	 
	-<xsl:import href="http://docbook.sourceforge.net/release/xsl/current/xhtml/docbook.xsl"/>
	+	<xsl:import href="file:///abs/path/to/docbook-xsl-1.76.1/xhtml/docbook.xsl"/>
	 
	 <xsl:param name="funcsynopsis.style">ansi</xsl:param>
	 <xsl:param name="citerefentry.link" select="'1'"></xsl:param>
	```
because `xsltproc` run with `--nonet` option.

4. Use gnu sed in `Makefile`

	```
	SED := gsed
	```
5. Finally use the script below to build the xhtml help pages.
In my example, I use `docbook-xml` installed from `port` to provide the dtd.
    ```shell
    #!/bin/bash

	dtd_mathml2=file://`pwd`/mathml2/mathml2.dtd
	dtd_dbmathml=file://`pwd`/dbmathml.dtd
	dtd_docbookx=file:///opt/local/share/xml/docbook/4.3/docbookx.dtd
	catalog_file=`pwd`/catalog
	
	xmlcatalog --create > "$catalog_file"
	
	xmlcatalog --noout --add public "-//W3C//DTD MathML 2.0//EN" "$dtd_mathml2" "$catalog_file"
	xmlcatalog --noout --add system "http://www.w3.org/TR/MathML2/dtd/mathml2.dtd" "$dtd_mathml2" "$catalog_file"
	xmlcatalog --noout --add public "-//OASIS//DTD DocBook MathML Module V1.1b1//EN" "$dtd_dbmathml" "$catalog_file"
	xmlcatalog --noout --add system "http://www.oasis-open.org/docbook/xml/mathml/1.1CR1/dbmathml.dtd" "$dtd_dbmathml" "$catalog_file"
	xmlcatalog --noout --add public "-//OASIS//DTD DocBook XML V4.3//EN" "$dtd_docbookx" "$catalog_file"
	xmlcatalog --noout --add system "http://www.oasis-open.org/docbook/xml/4.3b2/docbookx.dtd" "$dtd_docbookx" "$catalog_file"
	
	export XML_CATALOG_FILES=`pwd`/catalog

	echo "Using catalog file $XML_CATALOG_FILES"
	
	export ROOT=`pwd`/../man3
	make -C $ROOT -j10
	```
6. With the script above, we can get the xhtml documentations which can be viewed from browser. Follow the official guide to generate man pages output from xml like below
    ```shell
    $ xsltproc --noout --nonet docbook-xsl-1.76.1/manpages/docbook.xsl glAccum.xml
    ```

7. If you are also programming in OpenCL, we can use the Makefile below to generate man pages for OpenCL. The file `simplify-man.xsl` is from the official guide which can eliminate some errors.

    ```Makefile
	XMLS := $(wildcard *.xml)
	
	MANPAGES := $(patsubst %.xml,%.2,$(XMLS))
	
	%.2 : %.xml
    @xsltproc --nonet simplify-man.xsl $< | \
			xsltproc --nonet --noout /opt/local/share/xsl/docbook-xsl/manpages/docbook.xsl - 
	
	default: $(MANPAGES)

    ```
	    