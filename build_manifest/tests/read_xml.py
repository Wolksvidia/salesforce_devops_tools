import xml.etree.ElementTree as et
import os


all_reg = []
files = os.listdir('src/objects')
for file in files:
    if '-meta.xml' not in file:
        all_reg.append(file)

allfields = []
alllistv = []
allsharingr = []
allrecordt = []
allvalidr = []

for reg in all_reg:
    root = et.parse('src/objects/' + reg)
    root_tag = root.getroot().tag
    namespaces = root_tag[:root_tag.find('}')+1]
    reg_name = reg[:reg.find('.')]
    fields = root.findall(namespaces+'fields')
    for field in fields:
        allfields.append(reg_name+'.'+field.find(namespaces+'fullName').text)
    listviews = root.findall(namespaces+'listViews')
    for listview in listviews:
        alllistv.append(reg_name+'.'+listview.find(namespaces+'fullName').text)
    sharingreasons = root.findall(namespaces+'sharingReasons')
    for sharing in sharingreasons:
        allsharingr.append(reg_name+'.'+sharing.find(namespaces+'fullName').text)
    recordtypes = root.findall(namespaces+'recordTypes')
    for record in recordtypes:
        allrecordt.append(reg_name+'.'+record.find(namespaces+'fullName').text)
    validrules = root.findall(namespaces+'validationRules')
    for valid in validrules:
        allvalidr.append(reg_name+'.'+valid.find(namespaces+'fullName').text)

print(allfields)
print(alllistv)
print(allsharingr)
print(allrecordt)
print(allvalidr)