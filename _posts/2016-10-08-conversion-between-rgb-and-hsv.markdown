---
layout: post
title: Conversion between RGB and HSV
date: 2016-10-08 19:23:02 +0800
categories: graphics
---

Here is a Java re-implementation of RGB/HSV color conversion.

In order to see the result, I made a comparision between this implementation and AWT's implementation.

We can see the output result

> Our implementation
> [h = 80.0, s = 0.5, v = 0.6]
> [r = 0.5, g = 0.6, b = 0.3]
> 
> AWT implementation
> [80.259735, 0.503268, 0.6]
> [r = 0.5019607843137255, g = 0.6, b = 0.30196078431372547]


#### RGB to HSV

![RGB to HSV formula]({{ site.url }}/assets/img/rgb2hsv.png)

Following is the Java implementation for RGB to HSV formula

```java
public static Hsv rgb2hsv(Rgb rgb) {
	Hsv hsv = new Hsv();

	double max = Math.max(Math.max(rgb.r, rgb.g), rgb.b);
	double min = Math.min(Math.min(rgb.r, rgb.g), rgb.b);
	double delta = max - min;

	if (delta == 0) {
		hsv.h = 360;
		hsv.s = 0;
		hsv.v = max;
		return hsv;
	}

	if (max == rgb.r) {
		hsv.h = (rgb.g - rgb.b) / delta % 6;
	} else if (max == rgb.g) {
		hsv.h = (rgb.b - rgb.r) / delta + 2;
	} else {
		hsv.h = (rgb.r - rgb.g) / delta + 4;
	}
	hsv.h *= 60;

	if (max == 0) {
		hsv.s = 0;
	} else {
		hsv.s = delta / max;
	}

	hsv.v = max;

	return hsv;
}
```

#### HSV to RGB


![HSV to RGB formula]({{ site.url }}/assets/img/hsv2rgb.gif)

Following is the Java implementation for HSV to RGB formula

```java
public static Rgb hsv2rgb(Hsv hsv) {
	Rgb rgb = new Rgb();

	double hh = hsv.h / 60;
	int i = ((int) hh) % 6;

	double f = hh - i;
	double p = hsv.v * (1 - hsv.s);
	double q = hsv.v * (1 - f * hsv.s);
	double t = hsv.v * (1 - (1 - f) * hsv.s);

	switch (i) {
		case 0:
			rgb.r = hsv.v; rgb.g = t; rgb.b = q; break;
		case 1:
			rgb.r = q; rgb.g = hsv.v; rgb.b = p; break;
		case 2:
			rgb.r = p; rgb.g = hsv.v; rgb.b = t; break;
		case 3:
			rgb.r = p; rgb.g = q; rgb.b = hsv.v; break;
		case 4:
			rgb.r = t; rgb.g = p; rgb.b = hsv.v; break;
		case 5:
			rgb.r = hsv.v; rgb.g = p; rgb.b = q; break;
			default:
	}

	return rgb;
}
```

The full implementation can be found [here](https://gist.github.com/WanghongLin/4e4c457db5c63741a915280bcf78e1b7).

#### Reference
- [RGB to HSV conversion](http://math.stackexchange.com/questions/556341/rgb-to-hsv-color-conversion-algorithm)
- [C/C++ implementation RGB/HSV conversion](http://stackoverflow.com/questions/3018313/algorithm-to-convert-rgb-to-hsv-and-hsv-to-rgb-in-range-0-255-for-both)
