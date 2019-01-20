
import ctypes
from ctypes import c_char

__all__ = ['RID']

# The Record ID is 6 bytes in size. #
class RID(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ridParts', c_char *6 ),
     ]

    def __str__(self):
        #Parts = cast(self.ridParts,  c_char_p)
        '''    
        print self.ridParts[:1]
        print self.ridParts[:2]
        print self.ridParts[:3]
        print self.ridParts[:6]
        '''
        return "%02s%02s%02s%02s%02s%02s done" %(
                          self.ridParts[:1], self.ridParts[:2], self.ridParts[:3],
                          self.ridParts[:4], self.ridParts[:5], self.ridParts[:6] )

