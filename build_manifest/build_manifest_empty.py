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
        'quickActions':'QuickAction', 'remoteSiteSettings':'RemoteSiteSetting', 'workflows':'Workflow', 'dashboards':'Dashboard', 'reports':'Report',
        'cspTrustedSites':'CspTrustedSite',
        }

    """
    Non-implemented Metadata:
    'ApexComponent', 'CustomMetadata' (needs custom manipulation), 'CustomObjectTranslation', 'DuplicateRule', 
    'FlowCategory', 'GlobalValueSetTranslation', 'MatchingRules',
    """
    #read directory structure

    mdtypedirs = os.listdir(directory)

    nested_mdt_object = ['ValidationRule', 'CompactLayout', 'ListView', 'SharingReason', 'RecordType']
    nested_mdt_workflow = ['WorkflowFieldUpdate', 'WorkflowKnowledgePublish', 'WorkflowTask', 'WorkflowAlert', 'WorkflowSend', 'WorkflowOutboundMessage', 'WorkflowRule']

    # start our xml structure
    root = xml.Element('Package')
    root.set('xmlns','http://soap.sforce.com/2006/04/metadata')

    for mdtype in mdtypedirs:
        # create child node for each type of component
        if mdtype in METADATA_TYPE.keys():
            etype = xml.SubElement(root, 'types')
            ename = xml.SubElement(etype, 'name')
            ename.text = str(METADATA_TYPE[mdtype])
            emember = xml.SubElement(etype, 'members')
            emember.text = str('*')
            
            if mdtype == 'objects':
                for nest_mdtyp in nested_mdt_object:
                    etype = xml.SubElement(root, 'types')
                    ename = xml.SubElement(etype, 'name')
                    ename.text = nest_mdtyp
                    emember = xml.SubElement(etype, 'members')
                    emember.text = str('*')

            if mdtype == 'workflows':
                for nest_mdtyp in nested_mdt_workflow:
                    etype = xml.SubElement(root, 'types')
                    ename = xml.SubElement(etype, 'name')
                    ename.text = nest_mdtyp
                    emember = xml.SubElement(etype, 'members')
                    emember.text = str('*')

            #Custom behavior for custom labels
            if mdtype == 'labels':
                etype = xml.SubElement(root, 'types')
                ename = xml.SubElement(etype, 'name')
                ename.text = 'CustomLabel'
                emember = xml.SubElement(etype, 'members')
                emember.text = str('*')

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
    if args:
        custom_package_xml_generator(args[0], args[1])
    else:
        custom_package_xml_generator('src')