from .splice import Splice
from struct import unpack

PACKET_SIZE=188
SYNC_BYTE=b'\x47'

class Stream:
    def __init__(self,tsfile=None,show_null=True):
        self.splices=[]
        self.PID=False
        self.show_null=show_null
        self.parse_tsfile(tsfile)

    def parse_tsfile(self,tsfile):
        with open(tsfile,'rb') as tsdata:
            while tsdata:
                sync_chk=tsdata.read(1)
                if sync_chk==SYNC_BYTE:
                    packet =sync_chk+ tsdata.read(PACKET_SIZE-1)
                    if len(packet) == PACKET_SIZE:  self.parse_tspacket(packet)
                    else: break
                else: return 
                
                                
    def parse_tspacket(self,packet):
        # sync,two_bytes, one_byte = 4 byte header
        sync,two_bytes,one_byte, cue = unpack('>BHB184s', packet)
        tei = two_bytes >> 15
        pusi = two_bytes >> 14 & 0x1
        ts_priority = two_bytes >>13 & 0x1
        pid = two_bytes & 0x1fff
        scramble = one_byte >>6
        afc = (one_byte & 48) >> 4
        count = one_byte & 15
        if self.PID:
            if pid !=self.PID: return
        cue=cue[1:]
        if cue[0] !=0xfc : return 
        if cue[13]==0:
            if not self.show_null: return 
        try: tf=Splice(cue)
        except: return 
        tf.show()
        self.splices.append(tf)
        if not self.PID: self.PID=pid
        return 
            

