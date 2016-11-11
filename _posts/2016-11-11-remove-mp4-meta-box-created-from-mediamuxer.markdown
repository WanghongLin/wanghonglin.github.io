---
layout: post
title: Remove mp4 meta box created from MediaMuxer
date: 2016-11-11 11:13:45 +0800
categories: android
---

When create mp4 from MediaMuxer after Android 6.0, the MediaMuxer will insert the optional meta box in mp4.
But some old tool can not handle it. When using mp4info to see information in mp4 file, it will complain 
errors in meta box, like following output.

```
mp4info version 2.0.0
android16.mp4:
ReadAtom: "android16.mp4": invalid atom size, extends outside parent atom - skipping to end of "meta" "" 1753672424 vs 2260707
ReadAtom: "android16.mp4": atom type  is suspect
ReadChildAtoms: "android16.mp4": In atom meta missing child atom hdlr
ReadChildAtoms: "android16.mp4": In atom meta missing child atom ilst
Track	Type	Info
1	video	H264 High@1.3, 10.055 secs, 1735 kbps, 640x1136 @ 21.382397 fps
2	audio	MPEG-4 AAC LC, 9.616 secs, 96 kbps, 44100 Hz
ReadAtom: "android16.mp4": invalid atom size, extends outside parent atom - skipping to end of "meta" "" 1753672424 vs 2260707
ReadAtom: "android16.mp4": atom type  is suspect
ReadChildAtoms: "android16.mp4": In atom meta missing child atom hdlr
ReadChildAtoms: "android16.mp4": In atom meta missing child atom ilst
```

After read the standard and analyse the mp4 file, it seems the meta box is an optional box and it won't affect the decoding if
it's missing. mp4 files created by MediaMuxer prior Android 6.0 don't have meta box.

The meta box is located inside moov box, it's safe to remove. Following output is a part of heximal dump of moov box.

```
$ xxd android16.mp4 |grep -A 20 'moov'
0227df0: 28a7 a7ed b7ff 0000 227e 6d6f 6f76 0000  (......."~moov..
0227e00: 006c 6d76 6864 0000 0000 d448 d3c5 d448  .lmvhd.....H...H
0227e10: d3c5 0000 03e8 0000 2748 0001 0000 0100  ........'H......
0227e20: 0000 0000 0000 0000 0000 0001 0000 0000  ................
0227e30: 0000 0000 0000 0000 0000 0001 0000 0000  ................
0227e40: 0000 0000 0000 0000 0000 4000 0000 0000  ..........@.....
0227e50: 0000 0000 0000 0000 0000 0000 0000 0000  ................
0227e60: 0000 0000 0000 0000 0003 0000 0079 6d65  .............yme
0227e70: 7461 0000 0021 6864 6c72 0000 0000 0000  ta...!hdlr......
0227e80: 0000 6d64 7461 0000 0000 0000 0000 0000  ..mdta..........
0227e90: 0000 0000 0000 2b6b 6579 7300 0000 0000  ......+keys.....
0227ea0: 0000 0100 0000 1b6d 6474 6163 6f6d 2e61  .......mdtacom.a
0227eb0: 6e64 726f 6964 2e76 6572 7369 6f6e 0000  ndroid.version..
0227ec0: 0025 696c 7374 0000 001d 0000 0001 0000  .%ilst..........
0227ed0: 0015 6461 7461 0000 0001 0000 0000 362e  ..data........6.
0227ee0: 302e 3100 000c 2674 7261 6b00 0000 5c74  0.1...&trak...\t
0227ef0: 6b68 6400 0000 07d4 48d3 c5d4 48d3 c500  khd.....H...H...
0227f00: 0000 0100 0000 0000 0027 4800 0000 0000  .........'H.....
0227f10: 0000 0000 0000 0000 0000 0000 0100 0000  ................
0227f20: 0000 0000 0000 0000 0000 0000 0100 0000  ................
0227f30: 0000 0000 0000 0000 0000 0040 0000 0002  ...........@....
```

Then we can use the following code to remove the meta box, implemented in Java.

```java

public static void removeMetaBox(String inputFile, String outputFile) {
	try {
		FileInputStream inputStream = new FileInputStream(inputFile);
		byte[] originalBytes = new byte[inputStream.available()];
		if (inputStream.read(originalBytes) == originalBytes.length) {
			System.out.println("read whole file to byte arrays");
		}
		inputStream.close();

		int skipAtPosition = -1;
		int skipSize = 0;
		int moovSizePosition = -1;
		for (int i = 0; i < originalBytes.length; i++) {
			if (originalBytes[i] == MOOV_BOX[0]
					&& originalBytes[i+1] == MOOV_BOX[1]
					&& originalBytes[i+2] == MOOV_BOX[2]
					&& originalBytes[i+3] == MOOV_BOX[3]) {
				moovSizePosition = i - 4;
			}

			if (originalBytes[i] == META_BOX[0]
					&& originalBytes[i+1] == META_BOX[1]
					&& originalBytes[i+2] == META_BOX[2]
					&& originalBytes[i+3] == META_BOX[3]) {
				ByteBuffer buffer = ByteBuffer.allocate(4);
				buffer.put(originalBytes, i-4, 4).rewind();
				skipSize = buffer.asIntBuffer().get();
				skipAtPosition = i - 4;
				break;
			}
		}

		if (skipAtPosition != -1 && skipSize > 0) {
			FileOutputStream outputStream = new FileOutputStream(outputFile);
			System.out.println("find moov box size postion " + moovSizePosition);
			System.out.println("skip at " + skipAtPosition + " with size " + skipSize);
			if (moovSizePosition > 0) {
				ByteBuffer buffer = ByteBuffer.allocate(4);
				buffer.put(originalBytes, moovSizePosition, 4).rewind();
				int moovOldSize = buffer.asIntBuffer().get();
				int moovNewSize = moovOldSize - skipSize;
				buffer.rewind();
				buffer.asIntBuffer().put(moovNewSize).rewind();
				byte[] bytes = new byte[4];
				buffer.get(bytes);
				System.arraycopy(bytes, 0, originalBytes, moovSizePosition, 4);
				System.out.println("change moov box size from " + moovOldSize + " to " + moovNewSize);
			}

			byte[] modifiedBytes = new byte[originalBytes.length - skipSize];
			System.arraycopy(originalBytes, 0, modifiedBytes, 0, skipAtPosition);
			System.out.println("write first chunk " + skipAtPosition);
			System.arraycopy(originalBytes, skipAtPosition + skipSize, modifiedBytes, skipAtPosition, originalBytes.length - skipAtPosition - skipSize);
			System.out.println("write second chunk " + (originalBytes.length - skipAtPosition - skipSize));
			outputStream.write(modifiedBytes);
			outputStream.close();
		} else {
			System.out.println("meta box not found, not necessary to fix");
		}
	} catch (IOException e) {
		e.printStackTrace();
	}
}
```

After remove the meta box, use mp4info to see the mp4 information again, no errors complained.

```
$ mp4info android17.mp4 
mp4info version 2.0.0
android17.mp4:
Track	Type	Info
1	video	H264 High@1.3, 10.055 secs, 1735 kbps, 640x1136 @ 21.382397 fps
2	audio	MPEG-4 AAC LC, 9.616 secs, 96 kbps, 44100 Hz
```
