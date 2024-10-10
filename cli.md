 <h1>threefive is the SCTE-35 cli tool</h1>
   <br>

* [Help](#help) Display threefive help
* [Parse](#parse) Decode SCTE-35 Strings and MPEGTS
* [sixfix](#sixfix) sixfix changes Ffmpeg bin data back to SCTE-35. 
* [Version](#version) Display threefive version
* [Show](#show)  Show MPEGTS Stream information
* [PTS](#pts) Print PTS from MPEGTS Streams
* [Packets](#packets) Print Raw SCTE-35 packets
* [Sidecar](#sidecar) Create SCTE-35 sidecar files from MPEGTS
* [Encode](#encode) JSON to SCTE-35
* [Convert](#convert) SCTE-35 Formats (Base64 to Hex, etc...)


## `Help`
* Use the help man, I spent a lot of time trying to get it to make sense.

```lua
threefive help
```

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
___
* `Parse base64`
```js
threefive '/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo='
```

* `Parse a hex value`
```js
threefive 0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A
```

* `Parse MPEGTS from stdin`
```js
cat video.ts | threefive
```


* `Parse MPEGTS video over https`
```js
threefive https://so.slo.me/longb.ts
```


* `Parse multicast`
```lua
threefive udp://@235.35.3.5:3535


```

# keywords
the threefive cli uses keywords for additional functionality.

## `Version`

* keyword `version` - show threefive version
```lua
a@slow:~/threefive$ threefive version
2.4.35                                                                                           
a@slow:~/threefive$                                                                               
                           
```
---
## `Show`

* keyword `show`- display mpegts stream info

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
---
## `PTS`
* keyword `pts` -  display realtime program -> pts

```lua
a@fu:~$ threefive pts /home/a/msnbc.ts

1-> 3164.442756
1-> 3164.409422
1-> 3164.476089
1-> 3164.476089
1-> 3164.476089
1-> 3164.642756
1-> 3164.576089
```
---
## sixfix
* ffmpeg changes SCTE-35 streams types to 0x6 bin data. sixfix will convert the bin data back to SCTE-35.
* The new file name is prefixed with 'fixed'.
* As with all threefive, this works with local, http(s), UDP , and Multicast sources.


---
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
---

## `Packets`

* keyword `packets` - show raw SCTE-35 packets
```lua
a@slow:~/threefive$ threefive packets https://futzu.com/xaa.ts

b'G@\x86\x00\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x05\xdd\x01\x00\x00\xc0\xfc\xe7\x80\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
b'G@\x86\x01\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x07<\xeb\x00\x00\xbf\x8b\x96\x02\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
b'G@\x86\x02\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x08\x9c\xd5\x00\x00e\x07\x16F\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'

```
---
## `Sidecar`

* keyword `sidecar` - Generate a sidecar file of pts,cue pairs from a stream
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
---
## `Proxy`

* keyword `proxy` - parse the SCTE-35 from a stream and write it to stdout (for piping to ffmpeg and such)
```smalltalk
threefive proxy https://example.com/video.ts | ffmpeg -i - {ffmpeg commands}
```
---
## `Encode`
* keyword `encode` - Edit and Re-encode JSON output from threefive
The threefive cli tool can now encode JSON to SCTE-35. The JSON needs to be in threefive format. 

*  `a@fu:~$ threefive '/DAWAAAAAAAAAP/wBQb+ABt4xwAAwhCGHw==' 2> json.txt`

*  `cat json.txt`

```json
 {
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 22,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 0,
        "crc": "0xc210861f"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 20.004344
    },
    "descriptors": []
}

```
* Change the pts_time 
    * Here I do it with sed, you can use any editor 

```js
sed -i 's/20.004344/60.0/' json.txt
```
* Re-encode as Base64
```lua
a@fu:~$ cat json.txt | threefive encode

/DAWAAAAAAAAAP/wBQb+AFJlwAAAZ1PBRA==
```

* Re-encode as Hex
```lua
a@fu:~$ cat json.txt | threefive encode hex
0xfc301600000000000000fff00506fe005265c000006753c144
```

* Re-encode as an integer
```lua
a@fu:~$ cat json.txt | threefive encode int
1583008701074197245727019716796221242034694813189400685691204
```
* Re-encode as bytes
 ```lua
a@fu:~$ cat json.txt | threefive encode bytes
b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00Re\xc0\x00\x00gS\xc1D'
```
* Re-encode as Xml
```lua
cat json.txt | threefive encode xml

```

___
## `Convert`

* Convert Base64 SCTE-35 to Hex SCTE-35
* Converting involves piping one threefive command into another.
* `From`:
  * Base64
  * Hex
  * Json
  * Xml
* `To`
  * Base64
  * Bytes
  * Hex
  * Int
  * Json
  * Xml 

* `Base64` to `hex`
```js
a@fu:~$ prinf '/DAWAAAAAAAAAP/wBQb+ABt4xwAAwhCGHw==' | threefive encode hex
```
```js
0xfc301600000000000000fff00506fe001b78c70000c210861f
```
* `Hex` to `Integer`
```js
a@fu:~$ printf '0xfc301600000000000000fff00506fe001b78c70000c210861f'| threefive encode int
```
```js
1583008701074197245727019716796221242033681613329959740278303
```

* `Hex` to `Bytes`
```js

a@fu:~$ printf '0xfc301600000000000000fff00506fe001b78c70000c210861f'| threefive encode bytes
```
```js
b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x1bx\xc7\x00\x00\xc2\x10\x86\x1f'
```

* base64 to hex
```py3
  printf '/DBAAAGRZOeYAAAABQb+hJ8vqAAqAihDVUVJ/////3//AAAbX9ABFG1zbmJjX0VQMDQzMTEyMjEwNTU2EQEAbABeoQ==' |threefive encode hex
```
* hex to base64
```py3
printf 0xfc302500000000000000fff014050000013f7fefffffc3f680fe00a4cb80013f0000000063394f9c|  threefive encode 
```
* xml to base64
 ```py3
cat xml.xml | threefive encode
```
* xml to hex
 ```py3
cat xml.xml | threefive encode hex
```
* json to xml
```py3
cat json.json | threefive encode xml
```
* xml to json
```py3
cat xml.xml | threefive encode json
```
* xml to bytes
```py3
cat xml.xml | threefive encode bytes
---




