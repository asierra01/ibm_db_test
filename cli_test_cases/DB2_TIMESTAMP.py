from __future__ import absolute_import

from ctypes import Structure, c_short, c_ushort, c_int

__all__=['DB2_TIMESTAMP']

class DB2_TIMESTAMP(Structure):
    '''
     SQLSMALLINT   year;
     SQLUSMALLINT  month;
     SQLUSMALLINT  day
     SQLUSMALLINT  hour;
     SQLUSMALLINT  minute;
     SQLUSMALLINT  second;
     SQLUINTEGER   fraction;
    '''
    _pack_ = True
    _fields_ = [("year",     c_short),
                ("month",    c_ushort),
                ("day",      c_ushort),
                ("hour",     c_ushort),
                ("minute",   c_ushort),
                ("second",   c_ushort),
                ("fraction", c_int),
                ]

    def __init__(self):
        self.year     = 0
        self.month    = 0
        self.day      = 0
        self.hour     = 0
        self.minute   = 0
        self.second   = 0
        self.fraction = 0

    def __str__(self):
        #my_str = ""
        #YYYY-MM-DD
        return "%04d-%02d-%02d %d:%d:%d:%d" % (
           self.year, 
           self.month,
           self.day,
           self.hour,
           self.minute,
           self.second,
           self.fraction)


