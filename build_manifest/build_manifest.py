import xml.etree.ElementTree as xml
from xml.dom import minidom
import os
import sys


def custom_package_xml_generator(directory, packagename=None, version='45.0', filename='package.xml'):
    """Create custom package.xml file from directories with metadata"""

    METADATA_TYPE = {
        'applications':'CustomApplication', 'aura':'AuraDefinitionBundle',  'classes':'ApexClass', 'customPermissions':'CustomPermission', 
        'flexipages':'FlexiPage', 'flows':'Flow', 'globalValueSets':'GlobalValueSet', 'labels':'CustomLabels', 'layouts':'Layout',
        'lwc': 'LightningComponentBundle', 'objects':'CustomObject', 'pages':'ApexPage', 'permissionsets':'PermissionSet', 'profiles':'Profile',
        'staticresources':'StaticResource', 'tabs':'CustomTab', 'triggers':'ApexTrigger', 'contentassets':'ContentAsset', 'pathAssistants':'PathAssistant',
        'quickActions':'QuickAction', 'remoteSiteSettings':'RemoteSiteSetting', 'workflows':'Workflow'
        }

    """
    Non-implemented Metadata:
    'ApexComponent', 'CustomMetadata' (needs custom manipulation), 'CustomObjectTranslation', 'DuplicateRule', 
    'FlowCategory', 'GlobalValueSetTranslation', 'MatchingRules',

    <types>
        <name>Dashboard</name>
        <members>DreamHouse_Dashboards</members>
        <members>DreamHouse_Dashboards/PwhxKrnFNjvWCIHRklHhRcEIEyIIBm</members> #dentro de la carpeta del dashboard
    </types>
    <types>
        <name>Report</name>
        <members>DreamHouse_Reports</members>
        <members>DreamHouse_Reports/Days_on_Market</members>
        <members>DreamHouse_Reports/Portfolio_Health</members>
        <members>DreamHouse_Reports/Properties_by_Broker</members>
    </types>

    Workflow > Add 
    <types>
        <name>WorkflowFieldUpdate</name>
        <members>*</members>
    </types>
    <types>
        <name>WorkflowKnowledgePublish</name>
        <members>*</members>
    </types>
    <types>
        <name>WorkflowTask</name>
        <members>*</members>
    </types>
    <types>
        <name>WorkflowAlert</name>
        <members>*</members>
    </types>
    <types>
        <name>WorkflowSend</name>
        <members>*</members>
    </types>
    <types>
        <name>WorkflowOutboundMessage</name>
        <members>*</members>
    </types>
    <types>
        <name>WorkflowRule</name>
        <members>*</members>
    </types>
    """
    #read directory structure
    allfields = []
    alllistv = []
    allsharingr = []
    allrecordt = []
    allvalidr = []
    all_reg = []
    allclayout = []

    obj_dir = os.path.join(directory,'objects')

    dirs = os.listdir(directory)
    for dir in dirs:
        if os.path.isfile(os.path.join(directory,dir)) == False:
            all_reg.append([dir, os.listdir(os.path.join(directory, dir))])

    # start our xml structure
    root = xml.Element('Package')
    root.set('xmlns','http://soap.sforce.com/2006/04/metadata')

    for mdtype, mdnames in all_reg:
        # create child node for each type of component
        if mdtype in METADATA_TYPE.keys():
            etype = xml.SubElement(root, 'types')
            ename = xml.SubElement(etype, 'name')
            ename.text = str(METADATA_TYPE[mdtype])
            for member in mdnames:
                if '-meta.xml' not in member:
                    emember = xml.SubElement(etype, 'members')
                    index = member.find('.')
                    if index != -1:
                        emember.text = str(member[:index])
                    else:
                        emember.text = str(member)

                    #read custom metadata types for objects
                    if mdtype == 'objects':
                        obj = xml.parse(os.path.join(obj_dir,member))
                        root_tag = obj.getroot().tag
                        namespaces = root_tag[:root_tag.find('}')+1]
                        reg_name = member[:member.find('.')]
                        #serch fields
                        fields = obj.findall(namespaces+'fields')
                        for field in fields:
                            allfields.append(reg_name+'.'+field.find(namespaces+'fullName').text)
                        #serch listviews
                        listviews = obj.findall(namespaces+'listViews')
                        for listview in listviews:
                            alllistv.append(reg_name+'.'+listview.find(namespaces+'fullName').text)
                        #serach sharingreasons
                        sharingreasons = obj.findall(namespaces+'sharingReasons')
                        for sharing in sharingreasons:
                            allsharingr.append(reg_name+'.'+sharing.find(namespaces+'fullName').text)
                        #search recordtyps
                        recordtypes = obj.findall(namespaces+'recordTypes')
                        for record in recordtypes:
                            allrecordt.append(reg_name+'.'+record.find(namespaces+'fullName').text)
                        #search validationrules
                        validrules = obj.findall(namespaces+'validationRules')
                        for valid in validrules:
                            allvalidr.append(reg_name+'.'+valid.find(namespaces+'fullName').text)
                        #search contactlayouts
                        listclayouts = obj.findall(namespaces+'listViews')
                        for listclayout in listclayouts:
                            allclayout.append(reg_name+'.'+listclayout.find(namespaces+'fullName').text)

            #Custom behavior for custom labels
            if mdtype == 'labels':
                etype = xml.SubElement(root, 'types')
                ename = xml.SubElement(etype, 'name')
                ename.text = 'CustomLabel'
                emember = xml.SubElement(etype, 'members')
                emember.text = str('*')
    
    #add relateed metadata types for objects
    if allfields: #CustomField
        etype = xml.SubElement(root, 'types')
        ename = xml.SubElement(etype, 'name')
        ename.text = 'CustomField'
        for field in allfields: 
            emember = xml.SubElement(etype, 'members')
            emember.text = str(field)
            
    if allclayouts: #ContactLayouts
        etype = xml.SubElement(root, 'types')
        ename = xml.SubElement(etype, 'name')
        ename.text = 'CompactLayout'
        for field in allclayouts: 
            emember = xml.SubElement(etype, 'members')
            emember.text = str(field)

    if alllistv: #ListView
        etype = xml.SubElement(root, 'types')
        ename = xml.SubElement(etype, 'name')
        ename.text = 'ListView'
        for listv in alllistv:
            emember = xml.SubElement(etype, 'members')
            emember.text = str(listv)
            
    if allsharingr: #SharingReason
        etype = xml.SubElement(root, 'types')
        ename = xml.SubElement(etype, 'name')
        ename.text = 'SharingReason'
        for sharing in allsharingr:
            emember = xml.SubElement(etype, 'members')
            emember.text = str(sharing)
            
    if allrecordt: #RecordType
        etype = xml.SubElement(root, 'types')
        ename = xml.SubElement(etype, 'name')
        ename.text = 'RecordType'
        for record in allrecordt:
            emember = xml.SubElement(etype, 'members')
            emember.text = str(record)

    if allvalidr: #ValidationRule
        etype = xml.SubElement(root, 'types')
        ename = xml.SubElement(etype, 'name')
        ename.text = 'ValidationRule'
        for validr in allvalidr:
            emember = xml.SubElement(etype, 'members')
            emember.text = str(validr)

    # add the final xml node package.api_version
    eversion = xml.SubElement(root, 'version')
    eversion.text = str(version)

    #package name
    if packagename != None:
        efname = xml.SubElement(root, 'fullName')
        efname.text = str(packagename)

    #pretty format for xml
    xmlstring = xml.tostring(root)
    reparsed = minidom.parseString(xmlstring)
    prettyxml = reparsed.toprettyxml(indent='    ', newl='\n', encoding='UTF-8')
        
    #generate xml file from string
    try:
        with open(os.path.join(directory, filename), "bw") as xml_file:
            xml_file.write(prettyxml)
    except IOError:
        pass


if __name__ == '__main__':
    #custom_package_xml_generator('src', packagename='CMS Test Package')
    args = sys.argv[1:]
    custom_package_xml_generator(args[0], args[1])