# Encoding ( Requires threefive 2.2.65+ )


#### threefive.**Cue()**
##### A decoded Cue instance contains: 

* **cue.info_section** 1 [threefive.**SpliceInfoSection()**](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/section.py) instance

* **cue.command** 1 command instance
    * commands :  
        [ threefive.**BandwidthReservation()** ](https://github.com/futzu/SCTE35-threefive/blob/d3db590a99f01b3355309b6c83f47fde9801e79c/threefive/commands.py#L32)  , 
        [ threefive.**PrivateCommand()** ](https://github.com/futzu/SCTE35-threefive/blob/d3db590a99f01b3355309b6c83f47fde9801e79c/threefive/commands.py#L54)  , 
        [ threefive.**SpliceInsert()** ](https://github.com/futzu/SCTE35-threefive/blob/d3db590a99f01b3355309b6c83f47fde9801e79c/threefive/commands.py#L139)  , 
        [ threefive.**SpliceNull()** ](https://github.com/futzu/SCTE35-threefive/blob/d3db590a99f01b3355309b6c83f47fde9801e79c/threefive/commands.py#L43)  , 
        [ threefive.**TimeSignal()** ](https://github.com/futzu/SCTE35-threefive/blob/d3db590a99f01b3355309b6c83f47fde9801e79c/threefive/commands.py#L84)

* **cue.descriptors** a list of 0 or more descriptors instances
    * descriptors :  
        [ threefive.**AudioDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/2018430b11949895722ac7bd9ac6a5e042eab1ce/threefive/descriptors.py#L153)  , 
        [ threefive.**AvailDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/2018430b11949895722ac7bd9ac6a5e042eab1ce/threefive/descriptors.py#L50)  , 
        [ threefive.**DtmfDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/2018430b11949895722ac7bd9ac6a5e042eab1ce/threefive/descriptors.py#L78)  , 
        [ threefive.**SegmentationDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/2018430b11949895722ac7bd9ac6a5e042eab1ce/threefive/descriptors.py#L201)  , 
        [threefive.**TimeDescriptor()**](https://github.com/futzu/SCTE35-threefive/blob/2018430b11949895722ac7bd9ac6a5e042eab1ce/threefive/descriptors.py#L119)

* All instance vars can be accessed via dot notation.

```python3
>>>> from threefive import Cue
>>>> cue = Cue(b64)
>>>> cue.decode()
True
>>>> cue.command
{'command_length': 5, 'command_type': 6, 'name': 'Time Signal', 'time_specified_flag': True, 'pts_time': 22798.906911}
>>>> cue.command.pts_time
22798.906911
>>>> 
```

### Automatic Features

* Splice Info Section of the Cue is automatically generated. 
* length vars for Cue.command and Cue.descriptors are automatically generated.  
* Descriptor loop length and crc32 are automatically calculated 

## Examples

### Edit the Splice Insert Command in a Cue 
```python3
>>>> import threefive
>>>> Base64 = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="
>>>> cue = threefive.Cue(Base64)
>>>> cue.decode()
True
>>>> cue.command
{'command_length': 20, 'command_type': 5, 'name': 'Splice Insert', 'time_specified_flag': True, 'pts_time': 21514.559089, 'break_auto_return': True, 'break_duration': 60.293567, 'splice_event_id': 1207959695, 'splice_event_cancel_indicator': False, 'out_of_network_indicator': True, 'program_splice_flag': True, 'duration_flag': True, 'splice_immediate_flag': False, 'components': None, 'component_count': None, 'unique_program_id': 0, 'avail_num': 0, 'avail_expected': 0}

    # use dot notation to access values 
    
>>>> cue.command.break_duration = 90.0

   # Run cue.encode to generate new base64 string
      
>>>> cue.encode()
b'/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4Ae5igAAAAAAAKAAhDVUVJAAABNVB2fJs='


>>>> cue.show()
```
### Remove a Splice Descriptor in a Cue
```python3
>>>> import threefive
>>>> Base64 = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="
>>>> cue = threefive.Cue(Base64)
>>>> cue.decode()
True
>>>> cue.descriptors
[{'tag': 0, 'descriptor_length': 8, 'identifier': 'CUEI', 'name': 'Avail Descriptor', 'provider_avail_id': 309}]

   # cue.descriptors is a list

>>>> del cue.descriptors[0]
>>>> cue.descriptors
[]
>>>> cue.encode()
b'/DAlAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAAYinJUA=='
```
### Add a Dtmf Descriptor to an existing Cue
```python3
>>>> import threefive
>>>> Base64 = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="
>>>> cue = threefive.Cue(Base64)
>>>> cue.decode()
True
>>>> dscrptr = threefive.DtmfDescriptor()
>>>> dscrptr
{'tag': 1, 'descriptor_length': 0, 'identifier': None, 'bites': None, 'name': 'DTMF Descriptor', 'preroll': None, 'dtmf_count': None, 'dtmf_chars': []}

 # My data to load into the DtmfDescriptor instance

>>>> data = {'tag': 1, 'descriptor_length': 10, 'identifier': 'CUEI', 'name': 'DTMF Descriptor', 'preroll': 177, 'dtmf_count': 4, 'dtmf_chars': ['1'\
, '2', '1', '#']}

 #  Use threefive.tools.loader to load a dict or json data


>>>> threefive.tools.loader(dscrptr,data)

>>>> dscrptr
{'tag': 1, 'descriptor_length': 10, 'identifier': 'CUEI', 'bites': None, 'name': 'DTMF Descriptor', 'preroll': 177, 'dtmf_count': 4, 'dtmf_chars': ['1', '2', '1', '#']}


  # Append to cue.descrptors


>>>> cue.descriptors.append(dscrptr)
  # Run encode to generate new Base64 string
>>>> cue.encode()
b'/DA7AAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAWAAhDVUVJAAABNQEKQ1VFSbGfMTIxI55FecI='
```

## Cue with a Time Signal Command from scratch

```python3
>>>> import threefive
>>>> cmd = threefive.TimeSignal()
>>>> >>>> cmd
{'command_length': 0, 'command_type': 6, 'bites': None, 'name': 'Time Signal', 'time_specified_flag': None, 'pts_time': None}

     # set the values needed
     
>>>> cmd.time_specified_flag = True
>>>> cmd.pts_time = 23000.677777

  # Create an empty Cue

>>>> cue = threefive.Cue()

  # set cue.command to the TimeSignal Command cmd
  
>>>> cue.command = cmd

>>>> cue.encode()
b'/DAWAAAAAAAAAP/wBQb+e2KfxwAAN6nTrw=='

   #  run cue.show() to check values.
   
cue.show()
```

### Using threefive.Cue.load ( Requires threefive 2.2.67+)
* pass all Cue data at once 
* The format is the same as the output of Cue.decode()
```python3       
 {
      'info_section': {dict} ,
       'command': {dict},
        'descriptors': [list of {dicts}],
  }

```
* SpliceInfoSection is auto created if info_section is not present
* Command will be auto created if info_section dict has the key 'splice_command_type'
* Command will be auto created if command dict has the key 'command_type'
* descriptors will be auto created if each descriptor has the key 'tag'
* All length related variables are auto calculated.
* descriptor_loop_length, and crc are auto created.

```python3
>>>> from threefive import Cue

>>>> stuff = {
'info_section': {'table_id': '0xfc', 'section_syntax_indicator': False, 'private': False, 'sap_type': '0x3', 'sap_details': 'No Sap Type', 'section_length': 47, 'protocol_version': 0, 'encrypted_packet': False, 'encryption_algorithm': 0, 'pts_adjustment': 0.0, 'cw_index': '0xff', 'tier': '0xfff', 'splice_command_length': 20, 'splice_command_type': 5},

'command': {'command_length': 20, 'command_type': 5, 'name': 'Splice Insert', 'time_specified_flag': True, 'pts_time': 21514.559089, 'break_auto_return': True, 'break_duration': 60.293567, 'splice_event_id': 1207959695, 'splice_event_cancel_indicator': False, 'out_of_network_indicator': True, 'program_splice_flag': True, 'duration_flag': True, 'splice_immediate_flag': False, 'unique_program_id': 0, 'avail_num': 0, 'avail_expected': 0}, 

'descriptors': [{'tag': 0, 'descriptor_length': 8, 'identifier': 'CUEI', 'name': 'Avail Descriptor', 'provider_avail_id': 309}], 
}

>>>> cue = Cue()
>>>> cue.load(stuff)
>>>> cue.encode()
b'/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo='

>>>> cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 47,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0xff",
        "tier": "0xfff",
        "splice_command_length": 20,
        "splice_command_type": 5,
        "descriptor_loop_length": 10
    },
    "command": {
        "command_length": 20,
        "command_type": 5,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 21514.559089,
        "break_auto_return": true,
        "break_duration": 60.293567,
        "splice_event_id": 1207959695,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "unique_program_id": 0,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": [
        {
            "tag": 0,
            "descriptor_length": 8,
            "identifier": "CUEI",
            "name": "Avail Descriptor",
            "provider_avail_id": 309
        }
    ],
    "crc": "0x62dba30a"
}


```
