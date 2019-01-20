# -*- coding: utf-8 -*-
from utils import mylog

try:
    import xml.etree.ElementTree as ET
except TypeError as e:
    ET = None
    mylog.exception("importing xml.etree.ElementTree is throwing a TypeError excp %s" % e)
import sys
import io
import os

__all__ = ['LogXmlData']


class LogXmlData():
    """read the xml output of CALL SYSPROC.GET_CONFIG
    and save it to a string my_log_str later this string is save it to a file xml_out.txt
    """
    my_log_str = ""

    def __init__(self, filename):
        mylog.info("parsing xml file '%s' by xml.etree.ElementTree" % filename)
        if ET is None:
            mylog.warn("ET is None, xml.etree.ElementTree was not imported")
            return
        tree = ET.parse(filename)
        root = tree.getroot()
        #print root.tag
        first_dict = root[0][0][0]
        self.print_dic(first_dict, "")

    def log_something(self, child1, child2, space):
        """helper function"""
        some_text1 = child1.text.strip('\n').strip(' ').strip('\n')
        some_text2 = child2.text.strip('\n').strip(' ').strip('\n')
        mylog.debug("%s %s '%s'" % ( space ,some_text1,some_text2))
        if some_text1 == "Hint" and some_text2 == "":
            pass
        elif some_text1 == "Display Name":
            pass
        else:
            self.my_log_str += "%s %s : %s\n" % ( space, some_text1, some_text2)

    def print_dic(self, myroot, space):
        """recursively print the xml file
        """
        my_list = list(myroot)
        my_iterator = iter(my_list)
        space += "   "
        for child in my_iterator:
            child1 = child
            child2 = next(my_iterator)

            #  and  "Deferred Value Flags" in child1.text
            if child2.tag == "dict":
                #print len(child2)
                #print child2.tag
                for _i in range(len(child2)):
                    pass
                    #print child2[i].text ,i

                if child2[3].text.strip('\n').strip(' ').strip('\n') == "NONE":
                    #pass
                    #print "NONE"
                    continue
                if child2[1].text.strip('\n').strip(' ').strip('\n') == "Parameter Value":
                    #pass
                    _parameter_value = child2[3].text.strip('\n').strip(' ').strip('\n')
                    #print parameter_value
                    #sys.exit(0)xm    
                    #continue
            self.log_something(child1, child2, space)
            if child2.tag == 'dict':
                #print child2.tag
                self.print_dic(child2, space)

if __name__ == "__main__":

    if sys.version_info > (3,):
        unicode = str

    file_name = os.path.join("log", "xml_out.xml")
    if os.path.exists(file_name):
        mylog.info("loading file %s" % file_name)
        log_xml_data = LogXmlData(file_name)
        some_xm_file_normal = io.open(os.path.join("log", "xml_out.txt"), "w+", encoding="utf8")
        #print my_log_str
        some_xm_file_normal.write(unicode(log_xml_data .my_log_str))
        some_xm_file_normal.close()
    else:
        mylog.warn("xml file doesnt exist %s" % file_name)
    mylog.info("done")

    #mylog.info(my_log_str)