 <h1>threefive is the SCTE-35 cli tool</h1>
   <br>

* [Help](#help) Display threefive help.
* [HLS](#hls) Parse HLS for SCTE-35.
* [Parse](#parse) Decode SCTE-35 Strings and MPEGTS
* [Sixfix](#sixfix) sixfix converts Ffmpeg bin data streams back to SCTE-35.
* [Encode](#encode) JSON and XML as inputs for encoding to SCTE-35.
* [Xml](#xml) Xml as an output format for SCTE-35 Cues from strings and mpegts streams.
* [Version](#version) Display threefive version.
* [Show](#show)  Show MPEGTS Stream information.
* [PTS](#pts) Print PTS from MPEGTS Streams.
* [Packets](#packets) Print Raw SCTE-35 packets.
* [Sidecar](#sidecar) Create SCTE-35 sidecar files from MPEGTS.
* [Inject](#inject) Inject mpegts packets. 



## `Help`
* Use the help man, I spent a lot of time trying to get it to make sense.

`threefive help`

## `Parse` 


* By default, threefive will parse SCTE-35 from:
* Strings
	* Bytes
	* Base64
	* Hex
	* Integers
   
* MPEGTS 
	* Files
 	* Https
  	* Multicast
  	* UDP
  	* Stdin
            
* base64:     `threefive '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q=='`

* hex:        `threefive '0xfc301600000000000000fff00506fe00a98ac700000b3baed9'`

* files:      `threefive myvideo.ts`

* stdin:      `cat myvideo.ts | threefive`

* http(s):    `threefive https://futzu.com/xaa.ts`

* udp:        `threefive udp://127.0.0.1:3535`

* multicast:  `threefive udp://@235.35.3.5:3535`


[top](#threefive-is-the-scte-35-cli-tool)


# `KeyWords`
* the threefive cli uses keywords for additional functionality.

## `Version`
* keyword `version` - show threefive version

```js
 threefive version
```

[top](#threefive-is-the-scte-35-cli-tool)
___

## `Show`

* keyword `show`- display mpegts stream info
```js
 threefive show video.ts
```

 ```lua
a@fu:~$ threefive show https://futzu.com/xaa.ts

Program: 1
    Service:	Service01
    Provider:	FFmpeg
    Pid:	4096
    Pcr Pid:	256
    Streams:
		Pid: 134[0x86]	Type: 0x86 SCTE35 Data
		Pid: 256[0x100]	Type: 0x1b AVC Video
		Pid: 257[0x101]	Type: 0xf AAC Audio
```

[top](#threefive-is-the-scte-35-cli-tool)

---
## `PTS`
* keyword `pts` -  display realtime pts values
```py3
 threefive pts video.ts

```

[top](#threefive-is-the-scte-35-cli-tool)

___
## `Sixfix`
* keyword `sixfix` Fix SCTE-35 data mangled by ffmpeg.


```py3
	 threefive sixfix video.ts
```

* ffmpeg changes SCTE-35 streams types to 0x6 bin data.
![image](https://github.com/user-attachments/assets/d039debb-1a47-4c67-a98b-a77d4aa53435)

*  sixfix changes them back to SCTE-35.
* The new file name is prefixed with 'fixed'.


* Input file is sixed.ts

```js
  a@fu:~/build/SCTE35_threefive$ ffprobe -hide_banner sixed.ts                                    
Input #0, mpegts, from 'sixed.ts':                                                                                  
  Stream #0:0[0x100]: Video: h264 (Main) ([27][0][0][0] / 0x001B), yuv420p(tv, progressive), 640x360 [SAR 1:1 DAR 16:9], 29.97 fps, 29.97 tbr, 90k tbn
  Stream #0:1[0x101](und): Audio: aac (LC) ([15][0][0][0] / 0x000F), 48000 Hz, stereo, fltp, 64 kb/s
  Stream #0:2[0x102]: Data: bin_data ([6][0][0][0] / 0x0006) <------ Bin Data
  Stream #0:3[0x103]: Data: timed_id3 (ID3  / 0x20334449)
```
* Run  threefive sixfix
```js
a@fu:~/build/SCTE35_threefive$ ./threefive sixfix sixed.ts
```
* output file  is named fixed-sixed.ts
```js
a@fu:~/build/SCTE35_threefive$ ffprobe -hide_banner fixed-sixed.ts                            
Input #0, mpegts, from 'fixed-sixed.ts':                                                                            
  Stream #0:0[0x100]: Video: h264 (Main) ([27][0][0][0] / 0x001B), yuv420p(tv, progressive), 640x360 [SAR 1:1 DAR 16:9], 29.97 fps, 29.97 tbr, 90k tbn
  Stream #0:1[0x101](und): Audio: aac (LC) ([15][0][0][0] / 0x000F), 48000 Hz, stereo, fltp, 64 kb/s
  Stream #0:2[0x102]: Data: scte_35       <------------ fixed
  Stream #0:3[0x103]: Data: timed_id3 (ID3  / 0x20334449)
```

[top](#threefive-is-the-scte-35-cli-tool)

___

## `Encode`

* keyword `encode` -  Encode JSON, XML, Base64 or Hex __to__ JSON, XML, Base64, Hex, Int or Bytes.
___
* Example: __Change the pts_time__ 
    
* dump an existing Cue to json
```js
threefive 0xfc301600000000000000fff00506fe001b78c70000c210861f 2> json.json
```
* edit pts_time
     * Here I do it with sed, you can use any editor
```sed
sed -i 's/20.004344/60.0/' json.txt
```
* Re-encode as Base64
```lua
a@fu:~$ cat json.txt | threefive encode

/DAWAAAAAAAAAP/wBQb+AFJlwAAAZ1PBRA==
```
___
* Load JSON to base64:
  `threefive encode < json.json`
* Load JSON to hex:
  `threefive encode hex  < json.json`
* Load JSON to xml:
   `threefive encode xml < json.json`
* Load xml to hex:
  `cat xml.xml | threefive encode hex`
* Load xml to base64:
  `threefive encode  < xml.xml`
* Load xml to json:
  `cat xml.xml | threefive encode json`

* Base64 to bytes:
 `threefive encode bytes  '/DAlAAAAAAAAAP/wFAUAAAAOf+/+FOvVwP4ApMuAAA4AAAAAzBon0A=='`
* Base64 to hex:
   `threefive encode hex  '/DAlAAAAAAAAAP/wFAUAAAAOf+/+FOvVwP4ApMuAAA4AAAAAzBon0A=='`
* Base64 to xml:
   `threefive encode xml  '/DAlAAAAAAAAAP/wFAUAAAAOf+/+FOvVwP4ApMuAAA4AAAAAzBon0A=='`

* Hex to base64:
  `threefive encode base64 0xfc302500000000000000fff014050000000e7feffe14ebd5c0fe00a4cb80000e00000000cc1a27d0`
* Hex to xml:
  `threefive encode xml 0xfc302500000000000000fff014050000000e7feffe14ebd5c0fe00a4cb80000e00000000cc1a27d0`
* Hex to int:
  `threefive encode int 0xfc302500000000000000fff014050000000e7feffe14ebd5c0fe00a4cb80000e00000000cc1a27d0`

[top](#threefive-is-the-scte-35-cli-tool)

___

## `Xml`

* keyword `xml`  output Xml when decoding SCTE-35 data.

* xml output for Base64
```js
a@fu:~$ threefive xml  '/DAWAAAAAAAAAP/wBQb+ABt4xwAAwhCGHw=='
```
```xml 
<SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <TimeSignal>
      <SpliceTime ptsTime="1800391"/>
   </TimeSignal>
</SpliceInfoSection>
```
* Xml output is available when decoding mpegts streams using the xml keyword.
```js
a@fu:~$ threefive xml build/SCTE35_threefive/sixed.ts
```

[top](#threefive-is-the-scte-35-cli-tool)

___

## `Packets`

* keyword `packets` - show raw SCTE-35 packets

```lua
a@slow:~/threefive$ threefive packets https://futzu.com/xaa.ts

b'G@\x86\x00\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x05\xdd\x01\x00\x00\xc0\xfc\xe7\x80\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
b'G@\x86\x01\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x07<\xeb\x00\x00\xbf\x8b\x96\x02\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
b'G@\x86\x02\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x08\x9c\xd5\x00\x00e\x07\x16F\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'

```

[top](#threefive-is-the-scte-35-cli-tool)

___

## `Sidecar`
* keyword `sidecar` - Generate a sidecar file of pts,cue pairs from a stream.
```lua
  threefive sidecar https://futzu.com/xaa.ts
```

```lua
a@slow:~$ cat sidecar.txt
  
9.241178,/DAWAAAAAAAAAP/wBQb+AAy8lAAA2Olecw==
10.242178,/DAWAAAAAAAAAP/wBQb+AA4cfgAAquAlEw==
11.243178,/DAWAAAAAAAAAP/wBQb+AA98aAAAwU63WA==
12.244178,/DAWAAAAAAAAAP/wBQb+ABDcUgAAn3KLDA==
13.245178,/DAWAAAAAAAAAP/wBQb+ABI8PAAA11yRpQ==
14.246178,/DAWAAAAAAAAAP/wBQb+ABOcJgAAwqB4gg==
15.213811,/DAWAAAAAAAAAP/wBQb+ABT8EAAAIPU2sA==
16.214811,/DAWAAAAAAAAAP/wBQb+ABZb+gAATn6zuw==
17.215811,/DAWAAAAAAAAAP/wBQb+ABe75AAAjfN41Q==
18.216822,/DAWAAAAAAAAAP/wBQb+ABkb0AAAEwaiKg==
19.251189,/DAWAAAAAAAAAP/wBQb+ABp7ugAAs6FQDw==
20.218822,/DAWAAAAAAAAAP/wBQb+ABvbpAAAoT8LNA==
```

* [More on sidecar files](https://github.com/futzu/SCTE-35/blob/master/sidecar.md) 


[top](#threefive-is-the-scte-35-cli-tool)

___

## `Inject`
* Keyword `inject` `with` `at` inject SCTe-35 packets into MPEGTS video.
* format threefive inject [input mpegts] with [sidecar file] at [pid of new SCTE-35 stream]
```
threefive inject video.ts with sidecar.txt at 555
```
* Output file will be named `superkabuki-video.ts`
  
* [More on sidecar files](https://github.com/futzu/SCTE-35/blob/master/sidecar.md) 

[top](#threefive-is-the-scte-35-cli-tool)

___

## `HLS`
* keyword `hls`  parse MPEGTS and AAC HLS manifests and Segments for SCTE-35
```smalltalk
threefive hls https://example.com/master.m3u8
```
<details><summary> output  </summary>
	
![image](https://github.com/user-attachments/assets/176bcd7c-43d5-4d67-a0ff-45813b3718f7)


</details>


[top](#threefive-is-the-scte-35-cli-tool)

___


## `Proxy`

* keyword `proxy`  parse the SCTE-35 from a stream and write it to stdout (for piping to ffmpeg and such)
```smalltalk
threefive proxy https://example.com/video.ts | ffmpeg -i - {ffmpeg commands}
```
[top](#threefive-is-the-scte-35-cli-tool)

___

