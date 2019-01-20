from __future__ import absolute_import
from  ctypes import Structure, c_int, c_ushort, c_char


__all__ = ['TABLE_BULK_INSERT_DATA']

class TABLE_BULK_INSERT_DATA(Structure):
    _pack_ = True
    _fields_ = [("Cust_Num",     c_int),
                ("First_Name",   c_char * 21),
                ("Last_Name",    c_char * 21),
                ("Cust_Num_L",   c_int),
                ("First_Name_L", c_int),
                ("Last_Name_L",  c_int),
                ("rowStatus",    c_ushort),
                
                ]

    def __init__(self):
        self.Cust_Num = 0
        self.First_Name    = (c_char *21)() # create_string_buffer(21)
        self.Last_Name     = (c_char *21)()
        self.Cust_Num_L    = 0
        self.First_Name_L  = 0
        self.Last_Name_L   = 0
        self.rowStatus     = 0


    def __str__(self):
        return "%d '%-21s' '%-21s'" % (
           self.Cust_Num, 
           self.First_Name,
           self.Last_Name)

