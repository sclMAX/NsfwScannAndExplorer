import json
import codecs


def isVICValid(VIC={}):
    return (VIC.get('odata.metadata') and VIC.get('value'))

def readVICFromFile(VICFile):
    vic = json.load(codecs.open(VICFile, 'r', 'utf-8-sig'))
    if(isVICValid(vic)):
        return vic
    return None

def genNewMediaItem():
    return {
        'odata.id': '',
        'odata.editLink': '',
        'AlternativeHashes@odata.navigationLinkUrl': '',
        'AlternativeHashes': [],
        'Exifs@odata.navigationLinkUrl':  '',
        'Exifs': [],
        'MediaFiles': [
            {
                'odata.editLink': '',
                'Media@odata.navigationLinkUrl': '',
                'MD5': '',
                'FileName': '',
                'FilePath': '',
                'Created': None,
                'Written': None,
                'Accessed': None,
                'Unallocated': True
            }
        ],
        'MediaID': 0,
        'Category': None,
        'Comments': '',
        'VictimIdentified': None,
        'IsDistributed': None,
        'OffenderIdentified': None,
        'MD5': '',
        'Series': None,
        'SHA1': '',
        'Tags': '',
        'MediaSize': 0,
        'RelativeFilePath': '',
        'IsPrecategorized': False,
        'IsSuspected': False,
        'Miniature':''
    }

def updateMediaItem(mediaItem, data={}):
    if(mediaItem):
        for k in data:
            mediaItem[k] = data[k]

def updateMedia(VIC, newMedia):
    VIC['value'][0]['Media'] = newMedia

def getMediaFormVIC(VIC={}):
    return VIC['value'][0]['Media']
  
def genNewVic():
    return {
        'odata.metadata': 'http://github.com/ICMEC/ProjectVic/DataModels/1.3.xml#Cases',
        'value': [
            {
                'odata.id': '',
                'odata.editLink': '',
                'CaseMetadata@odata.navigationLinkUrl': '',
                'CaseMetadata': [
                    {
                        'odata.editLink': '',
                        'Case@odata.navigationLinkUrl': '',
                        'CaseID': '',
                        'PropertyName': '',
                        'PropertyValue': ''
                    }
                ],
                'Media@odata.navigationLinkUrl': '',
                'Media': [
                    {
                        'odata.id': '',
                        'odata.editLink': '',
                        'AlternativeHashes@odata.navigationLinkUrl': '',
                        'AlternativeHashes': [],
                        'Exifs@odata.navigationLinkUrl': '',
                        'Exifs': [],
                        'MediaFiles': [
                            {
                                'odata.editLink': '',
                                'Media@odata.navigationLinkUrl': '',
                                'MD5': '',
                                'FileName': '',
                                'FilePath': '',
                                'Created': None,
                                'Written': None,
                                'Accessed': None,
                                'Unallocated': True
                            }
                        ],
                        'MediaID': 0,
                        'Category': None,
                        'Comments': '',
                        'VictimIdentified': None,
                        'IsDistributed': None,
                        'OffenderIdentified': None,
                        'MD5': '',
                        'Series': None,
                        'SHA1': '',
                        'Tags': '',
                        'MediaSize': '',
                        'RelativeFilePath': '',
                        'IsPrecategorized': False,
                        'IsSuspected': False
                    }
                ],
                'CaseID': '',
                'CaseNumber': '',
                'ContactOrganization': '',
                'ContactName': '',
                'ContactPhone': '',
                'ContactEmail': '',
                'ContactTitle': '',
                'TotalMediaFiles': 0,
                'TotalPrecategorized': 0,
                'SeizureDate': '',
                'SourceApplicationName': '',
                'SourceApplicationVersion': ''
            }
        ]
    }

def getVicCaseData(inVIC):
    VIC = inVIC.get('value')
    VIC = VIC[0]
    txt:str='Case Nº: %s \t\t ID: %s\n' %(VIC.get('CaseNumber'), VIC.get('CaseID'))
    txt +=  'Contact Organization: %s\n'  %(VIC.get('ContactOrganization'))
    txt +=  'Contact Name: %s \t\t Title: %s\n'  %(VIC.get('ContactName'),VIC.get('ContactTitle'))      
    txt +=  'Contact Email: %s \t\t Phone: %s\n'  %(VIC.get('ContactEmail'),VIC.get('ContactPhone')) 
    txt +=  '\nTotal Media Files: %s \t\t Precategorized: %s\n'  %(VIC.get('TotalMediaFiles'),VIC.get('TotalPrecategorized')) 
    txt +=  'SeizureDate: %s \t SourceApplicationName: %s \t SourceApplicationVersion: %s\n\n'  %(VIC.get('SeizureDate'),VIC.get('SourceApplicationName'),VIC.get('SourceApplicationVersion'))
    return txt
