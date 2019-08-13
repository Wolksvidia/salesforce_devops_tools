from lxml import etree
import xml.etree.ElementTree as et
import os


def custom_package_xml_generator(version='45.0', packagename=None, directory='src', filename='package.xml'):
    """Create custom package.xml file from directories with metadata"""

    METADATA_TYPE = {
        'applications':'CustomApplication', 'aura':'AuraDefinitionBundle',  'classes':'ApexClass', 'customPermission':'CustomPermission', 
        'flexipages':'FlexiPage', 'flows':'Flow', 'globalValueSets':'GlobalValueSet', 'labels':'CustomLabels', 'layouts':'Layout',
        'lwc': 'LightningComponentBundle', 'objects':'CustomObject', 'pages':'ApexPage', 'permissionsets':'PermissionSet', 'profiles':'Profile',
        'staticresources':'StaticResource', 'tabs':'CustomTab', 'triggers':'ApexTrigger' 
        }

    """ 
    Non-implemented Metadata:
    'ApexComponent', 'CustomMetadata' (needs custom manipulation), 'CustomObjectTranslation','CustomPermission', 'DuplicateRule', 
    'FlowCategory', 'GlobalValueSetTranslation', 'MatchingRules', 'PathAssistant', 'CompactLayout'
    """
    #read directory structure
    allfields = []
    alllistv = []
    allsharingr = []
    allrecordt = []
    allvalidr = []
    all_reg = []
    dirs = os.listdir(directory)
    for dir in dirs:
        if '.xml' not in dir:
            all_reg.append([dir, os.listdir(directory +'/'+ dir)])

    # start our xml structure
    root = etree.Element('Package')
    root.set('xmlns','http://soap.sforce.com/2006/04/metadata')

    for mdtype, mdnames in all_reg:
        # create child node for each type of component
        if mdtype in METADATA_TYPE.keys():
            top_child = etree.Element('types')
            child = etree.Element('name')
            child.text = str(METADATA_TYPE[mdtype])
            top_child.append(child)
            for member in mdnames:
                if '-meta.xml' not in member:
                    child = etree.Element('members')
                    index = member.find('.')
                    if index != -1:
                        child.text = str(member[:index])
                    else:
                        child.text = str(member)
                    top_child.append(child)

                    #read custom metadata types for objects
                    if mdtype == 'objects':
                        obj = et.parse(directory+'/objects/'+member)
                        root_tag = obj.getroot().tag
                        namespaces = root_tag[:root_tag.find('}')+1]
                        reg_name = member[:member.find('.')]
                        fields = obj.findall(namespaces+'fields')
                        for field in fields:
                            allfields.append(reg_name+'.'+field.find(namespaces+'fullName').text)
                        listviews = obj.findall(namespaces+'listViews')
                        for listview in listviews:
                            alllistv.append(reg_name+'.'+listview.find(namespaces+'fullName').text)
                        sharingreasons = obj.findall(namespaces+'sharingReasons')
                        for sharing in sharingreasons:
                            allsharingr.append(reg_name+'.'+sharing.find(namespaces+'fullName').text)
                        recordtypes = obj.findall(namespaces+'recordTypes')
                        for record in recordtypes:
                            allrecordt.append(reg_name+'.'+record.find(namespaces+'fullName').text)
                        validrules = obj.findall(namespaces+'validationRules')
                        for valid in validrules:
                            allvalidr.append(reg_name+'.'+valid.find(namespaces+'fullName').text)

            # append metadata type to xml
            root.append(top_child)

            #Custom behavior for custom labels
            if mdtype == 'labels':
                top_child = etree.Element('types')
                child = etree.Element('name')
                child.text = str('CustomLabel')
                top_child.append(child)
                child = etree.Element('members')
                child.text = str('*')
                top_child.append(child)
                root.append(top_child)
    
    #add relateed metadata types for objects
    if allfields: #CustomField
        top_child = etree.Element('types')
        child = etree.Element('name')
        child.text = str('CustomField')
        top_child.append(child)
        for field in allfields: 
            child = etree.Element('members')
            child.text = str(field)
            top_child.append(child)
        root.append(top_child)
    if alllistv: #ListView
        top_child = etree.Element('types')
        child = etree.Element('name')
        child.text = str('ListView')
        top_child.append(child)
        for listv in alllistv:
            child = etree.Element('members')
            child.text = str(listv)
            top_child.append(child)
        root.append(top_child)
    if allsharingr: #SharingReason
        top_child = etree.Element('types')
        child = etree.Element('name')
        child.text = str('SharingReason')
        top_child.append(child)
        for sharing in allsharingr:
            child = etree.Element('members')
            child.text = str(sharing)
            top_child.append(child)
        root.append(top_child)
    if allrecordt: #RecordType
        top_child = etree.Element('types')
        child = etree.Element('name')
        child.text = str('RecordType')
        top_child.append(child)
        for record in allrecordt:
            child = etree.Element('members')
            child.text = str(record)
            top_child.append(child)
        root.append(top_child)
    if allvalidr: #ValidationRule
        top_child = etree.Element('types')
        child = etree.Element('name')
        child.text = str('ValidationRule')
        top_child.append(child)
        for validr in allvalidr:
            child = etree.Element('members')
            child.text = str(validr)
            top_child.append(child)
        root.append(top_child)

    # add the final xml node package.api_version
    child = etree.Element('version')
    child.text = str(version) 
    root.append(child)

    #package name
    if packagename != None:
        child = etree.Element('fullName')
        child.text = str(packagename) 
        root.append(child)

    # create file string
    obj_xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    #generate xml file from string
    try:
        with open(filename, "wb") as xml_file:
            xml_file.write(obj_xml)
    except IOError:
        pass

#custom_package_xml_generator(packagename='CMS Test Package')
custom_package_xml_generator()