#!/usr/bin/python3
import sys
import re


if len(sys.argv) != 3:
    print ("Usage: %s <path to diskbyid output> <path to LSI output>" % sys.argv[0])
    sys.exit(0)

guid_devid_map=dict()
guid_encl_slot_map=dict()
ansi_escape = re.compile(r'\x1b[^m]*m')

def create_guid_dev_id_map(diskByIDFile):
    """Reads output of diskbyid and maps GUID to device id """
    wwn_regex = r'wwn-0x(\w+).+$'
    with open(diskByIDFile) as f:
        for line in f:
            stripped = line.rstrip('\n')
            match = re.search(wwn_regex, stripped) 
            if match != None:
                guid_devid_map[match.group(1)] = stripped[-4:]

def create_guid_encl_slot_map(lsiOutputFile):
    """Reads LSI config output and maps GUID to enclosure and slot number """
    scan = 0
    with open(lsiOutputFile) as f:
        for line in f:
            stripped = line.rstrip('\n')
            if stripped.find('Device') >= 0:
                scan = 1
            if scan and (stripped.find('Slot #') > 0):
                slot = stripped.split(':')[1].strip()
            if scan and (stripped.find('GUID') > 0):
                guid_encl_slot_map[stripped.split(':')[1].strip()] = slot
                scan = 0

def print_mapping():
    for key in guid_encl_slot_map.keys():
        print("%s --> %s" % (guid_encl_slot_map[key], guid_devid_map[key])) 

create_guid_dev_id_map(sys.argv[1])
create_guid_encl_slot_map(sys.argv[2])
print_mapping()
