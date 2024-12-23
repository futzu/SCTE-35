"""
threefive.Cue Class
"""

from base64 import b64decode, b64encode
import json
from .stuff import print2
from .bitn import NBin
from .base import SCTE35Base
from .section import SpliceInfoSection
from .commands import command_map
from .descriptors import splice_descriptor, descriptor_map
from .crc import crc32
from .xml import Node, XmlParser
from .segmentation import table22


class Cue(SCTE35Base):
    """
    The threefive.Splice class handles parsing
    SCTE 35 message strings.
    Example usage:

    >>>> import threefive
    >>>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
    >>>> cue = threefive.Cue(Base64)

    # cue.decode() returns True on success,or False if decoding failed

    >>>> cue.decode()
    True

    # After Calling cue.decode() the instance variables can be accessed via dot notation.

    >>>> cue.command
    {'command_length': 5, 'name': 'Time Signal', 'time_specified_flag': True,
    'pts_time': 21695.740089}

    >>>> cue.command.pts_time
    21695.740089

    >>>> cue.info_section.table_id

    '0xfc'

    """

    def __init__(self, data=None, packet_data=None):
        """
        data may be packet bites or encoded string
        packet_data is a instance passed from a Stream instance
        """
        self.command = None

        self.descriptors = []
        self.info_section = SpliceInfoSection()
        self.bites = None
        if data:
            self.bites = self._mk_bits(data)
        self.packet_data = packet_data
        self.dash_data = None

    def __repr__(self):
        return str(self.__dict__)

    # decode

    def decode(self):
        """
        Cue.decode() parses for SCTE35 data
        """
        bites = self.bites
        self.descriptors = []
        while bites:
            bites = self.mk_info_section(bites)
            bites = self._set_splice_command(bites)
            bites = self._mk_descriptors(bites)
            crc = hex(int.from_bytes(bites[0:4], byteorder="big"))
            self.info_section.crc = crc
            return True
        return False

    def _descriptor_loop(self, loop_bites):
        """
        Cue._descriptor_loop parses all splice descriptors
        """
        tag_n_len = 2
        while len(loop_bites) > tag_n_len:
            spliced = splice_descriptor(loop_bites)
            if not spliced:
                return
            sd_size = tag_n_len + spliced.descriptor_length
            loop_bites = loop_bites[sd_size:]
            del spliced.bites
            self.descriptors.append(spliced)

    def _get_dash_data(self, scte35_dict):
        if self.dash_data:
            scte35_dict["dash_data"] = self.dash_data
        return scte35_dict

    def _get_packet_data(self, scte35_dict):
        if self.packet_data:
            scte35_dict["packet_data"] = self.packet_data.get()
        return scte35_dict

    def get(self):
        """
        Cue.get returns the SCTE-35 Cue
        data as a dict of dicts.
        """
        if self.command and self.info_section:
            scte35 = {
                "info_section": self.info_section.get(),
                "command": self.command.get(),
                "descriptors": self.get_descriptors(),
            }
            scte35 = self._get_dash_data(scte35)
            scte35 = self._get_packet_data(scte35)
            return scte35
        return False

    def get_descriptors(self):
        """
        Cue.get_descriptors returns a list of
        SCTE 35 splice descriptors as dicts.
        """
        return [d.get() for d in self.descriptors]

    def get_json(self):
        """
        Cue.get_json returns the Cue instance
        data in json.
        """
        return json.dumps(self.get(), indent=4)

    def get_bytes(self):
        """
        get_bytes returns Cue.bites
        """
        return self.bites

    @staticmethod
    def fix_bad_b64(data):
        """
        fix_bad_b64 fixes bad padding on Base64
        """
        while len(data) % 4 != 0:
            data = data + "="
        return data

    def _int_bits(self, data):
        length = data.bit_length() >> 3
        bites = int.to_bytes(data, length, byteorder="big")
        return bites

    def _hex_bits(self, data):
        try:
            i = int(data, 16)
            i_len = i.bit_length() >> 3
            bites = int.to_bytes(i, i_len, byteorder="big")
            return bites
        except (LookupError, TypeError, ValueError):
            if data[:2].lower() == "0x":
                data = data[2:]
            if data[:2].lower() == "fc":
                return bytes.fromhex(data)
        return b""

    def _b64_bits(self, data):
        try:
            return b64decode(self.fix_bad_b64(data))
        except (LookupError, TypeError, ValueError):
            return data

    def _str_bits(self, data):
        try:
            self.load(data)
            return self._mk_load(data)
        except:
            hex_bits = self._hex_bits(data)
            if hex_bits:
                return hex_bits
        return self._b64_bits(data)

    def _mk_load(self, data):
        """
         _mk_load sets self.bytes when loading
        data. Encode is called to set missing fields
        when possible and re-calc the length vars and crc.
        """
       # pass
       # print2("_mk_load")
       # if self.load(data):
        #bites = self.bites
       # self.encode()
        #return bites
        return data


    def _mk_bits(self, data):
        """
        cue._mk_bits Converts
        Hex and Base64 strings into bytes.
        """
        if isinstance(data, bytes):
            return self.idxsplit(data, b"\xfc")
        if isinstance(data, int):
            return self._int_bits(data)
        if isinstance(data, dict):
            return self._mk_load(data)
        if isinstance(data, Node):
            return self._mk_load(data.mk())
        if isinstance(data, str):
            return self._str_bits(data)

    def _mk_descriptors(self, bites):
        """
        Cue._mk_descriptors parses
        Cue.info_section.descriptor_loop_length,
        then call Cue._descriptor_loop
        """
        if len(bites) < 2:
            return False
        dll = (bites[0] << 8) | bites[1]
        self.info_section.descriptor_loop_length = dll
        bites = bites[2:]
        self._descriptor_loop(bites[:dll])
        return bites[dll:]

    def mk_info_section(self, bites):
        """
        Cue.mk_info_section parses the
        Splice Info Section
        of a SCTE35 cue.
        """
        info_size = 14
        info_bites = bites[:info_size]
        self.info_section.decode(info_bites)
        return bites[info_size:]

    def _set_splice_command(self, bites):
        """
        Cue._set_splice_command parses
        the command section of a SCTE35 cue.
        """
        sct = self.info_section.splice_command_type
        if sct not in command_map:
            return False
        iscl = self.info_section.splice_command_length
        cmd_bites = bites[:iscl]
        self.command = command_map[sct](cmd_bites)
        self.command.command_length = iscl

        self.command.decode()
        del self.command.bites
        return bites[iscl:]

    # encode related

    def encode(self):
        """
        Cue.encode() converts SCTE35 data
        to a base64 encoded string.
        """
        dscptr_bites = self._unloop_descriptors()
        dll = len(dscptr_bites)
        self.info_section.descriptor_loop_length = dll
        if not self.command:
            self.no_cmd()
        cmd_bites = self.command.encode()
        cmdl = self.command.command_length = len(cmd_bites)
        self.info_section.splice_command_length = cmdl
        self.info_section.splice_command_type = self.command.command_type
        # 11 bytes for info section + command + 2 descriptor loop length
        # + descriptor loop + 4 for crc
        self.info_section.section_length = 11 + cmdl + 2 + dll + 4
        self.bites = self.info_section.encode()
        self.bites += cmd_bites
        self.bites += int.to_bytes(
            self.info_section.descriptor_loop_length, 2, byteorder="big"
        )
        self.bites += dscptr_bites
        self._encode_crc()
        return b64encode(self.bites).decode()

    def encode_as_int(self):
        """
        encode_as_int returns self.bites as an int.
        """
        self.encode()
        return int.from_bytes(self.bites, byteorder="big")

    def encode2int(self):
        """
        encode2int returns self.bites as an int.
        """
        return self.encode_as_int()

    def encode_as_hex(self):
        """
        encode_as_hex returns self.bites as
        a hex string
        """
        return hex(self.encode_as_int())

    def encode2hex(self):
        """
        encode2hex returns self.bites as
        a hex string
        """
        return hex(self.encode2int())

    def _encode_crc(self):
        """
        _encode_crc encode crc32
        """
        crc_int = crc32(self.bites)
        self.info_section.crc = hex(crc_int)
        self.bites += int.to_bytes(crc_int, 4, byteorder="big")

    def _unloop_descriptors(self):
        """
        _unloop_descriptors
        for each descriptor in self.descriptors
        encode descriptor tag, descriptor length,
        and the descriptor into all_bites.bites
        """
        all_bites = NBin()
        dbite_chunks = [dsptr.encode() for dsptr in self.descriptors]
        for chunk, dsptr in zip(dbite_chunks, self.descriptors):
            dsptr.descriptor_length = len(chunk)
            all_bites.add_int(dsptr.tag, 8)
            all_bites.add_int(dsptr.descriptor_length, 8)
            all_bites.add_bites(chunk)
        return all_bites.bites

    def load_info_section(self, stuff):
        """
        load_info_section loads data for Cue.info_section
        isec should be a dict.
        if 'splice_command_type' is included,
        an empty command instance will be created for Cue.command
        """
        if "info_section" in stuff:
            self.info_section.load(stuff["info_section"])

    def load_command(self, stuff):
        """
        load_command loads data for Cue.command
        cmd should be a dict.
        if 'command_type' is included,
        the command instance will be created.
        """
        if "command" not in stuff:
            self.no_cmd()
        cmd = stuff["command"]
        if "command_type" in cmd:
            self.command = command_map[cmd["command_type"]]()
            self.command.load(cmd)

    def load_descriptors(self, dlist):
        """
        Load_descriptors loads descriptor data.
        dlist is a list of dicts
        if 'tag' is included in each dict,
        a descriptor instance will be created.
        """
        if not isinstance(dlist, list):
            raise Exception("\033[7mdescriptors should be a list\033[27m")
        for dstuff in dlist:
            if "tag" in dstuff:
                dscptr = descriptor_map[dstuff["tag"]]()
                dscptr.load(dstuff)
                self.descriptors.append(dscptr)

    def no_cmd(self):
        """
        no_cmd raises an exception if no splice command.
        """
        raise Exception("\033[7mA splice command is required\033[27m")

    def load(self, stuff):
        """
        Cue.load loads SCTE35 data for encoding.
        stuff is a dict or json
        with any or all of these keys
        stuff = {
            'info_section': {dict} ,
            'command': {dict},
            'descriptors': [list of {dicts}],
            }
        """
        if isinstance(stuff, str):
            if stuff.strip()[0] == "<":
                xmlp = XmlParser()
                cue_data = xmlp.parse(stuff)
                self.from_xml(cue_data)
                return True
            stuff = json.loads(stuff)
        if "command" not in stuff:
            self.no_cmd()
        self.load_info_section(stuff)
        self.load_command(stuff)
        self.load_descriptors(stuff["descriptors"])
        self.encode()
        return True

    # Dash

    def _xml_splice_info_section(self, stuff):
        if "SpliceInfoSection" in stuff:
            self.info_section = SpliceInfoSection()
            self.info_section.from_xml(stuff)

    def _xml_from_map(self, a_map, b_map, stuff):
        for k, v in a_map.items():
            if k in stuff:
                made = b_map[v]()
                made.from_xml(stuff)
                return made
        return False

    def _xml_splice_command(self, stuff):
        cmap = {
            "BandwidthReservation": 7,
            "PrivateCommand": 255,
            "SpliceInsert": 5,
            "SpliceNull": 0,
            "TimeSignal": 6,
        }
        self.command = self._xml_from_map(cmap, command_map, stuff)

    def _xml_splice_descriptors(self, stuff):
        dmap = {
            "SegmentationDescriptor": 2,
            "AvailDescriptor": 0,
            "DTMFDescriptor": 1,
            "TimeDescriptor": 3,
        }
        for dstuff in stuff["descriptors"]:
            self.descriptors.append(self._xml_from_map(dmap, descriptor_map, dstuff))

    def _xml_event_signal(self, stuff):
        self.dash_data = {}
        for x in ["EventStream", "Event", "Signal", "Binary"]:
            if x in stuff:
                self.dash_data[x] = stuff[x]

    def _xml_assemble(self, stuff):
        self._xml_splice_info_section(stuff)
        self._xml_splice_command(stuff)
        self.info_section.splice_command_type = self.command.command_type
        self._xml_splice_descriptors(stuff)

    def from_xml(self, stuff):
        """
        build_cue takes the data put into the stuff dict
        and builds a threefive.Cue instance
        """
        self._xml_event_signal(stuff)
        if "Binary" in stuff:
            self.bites = self._mk_bits(stuff["Binary"]["binary"])
            self.decode()
        else:
            self._xml_assemble(stuff)
            # Self.encode() will calculate lengths and types and such
            self.encode()

    def _xmlbin(self, ns):
        sig_attrs = {"xmlns": "https://scte.org/schemas/35"}
        sig_node = Node("Signal", attrs=sig_attrs, ns=ns)
        bin_node = Node("Binary", value=self.encode(), ns=ns)
        sig_node.add_child(bin_node)
        return sig_node

    def _xml_mk_descriptor(self, sis, ns):
        """
        _mk_descriptor_xml make xml nodes for descriptors.
        """
        for d in self.descriptors:
            if d.has("segmentation_type_id") and d.segmentation_type_id in table22:
                comment = f"{table22[d.segmentation_type_id]}"
                sis.add_comment(comment)
            sis.add_child(d.xml(ns=ns))
        return sis

    def xml(self, ns="scte35", xmlbin=True):
        """
        xml returns a threefive.Node instance
        which can be edited as needed or printed.
        xmlbin
        """
        if xmlbin:
            return self._xmlbin(ns=ns)
        sis = self.info_section.xml(ns=ns)
        # if not self.command:
        #    raise Exception("\033[7mA Splice Command is Required\033[27m")
        cmd = self.command.xml(ns=ns)
        sis.add_child(cmd)
        sis = self._xml_mk_descriptor(sis, ns)
        sis.mk()
        return sis
