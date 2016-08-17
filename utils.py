## Various functions and classes for using XMLgen with SigMond
import xml.etree.cElementTree as ET
import os


# # UNFINISHED - CLASSES FOR MCOBSERVABLES, OPERATORS, ETC??
# class ()

# Indent for easy reading
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
