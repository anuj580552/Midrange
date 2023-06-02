"""Jinja2 template to generate the jython script.

The extension of this file has been choosen to be py... This will enable 
the suported editing tools for python.

The Global variables are passed by the calling module.
"""
import sys
from com.ibm.websphere.management.exception import AdminException

# End - Global variable 

# Input variables passed by call script
{% if inventory_hostname_short is defined %}
# setup hostname
hostName = '{{ inventory_hostname_short }}'
{% else %}
hostName = 'Error hostname not provided'
{% endif %}
{% if scopeType is defined %}
# setup scopeType
scopeType = '{{ scopeType }}'
{% else %}
# scopetype is not defined... assume dmgr
scopeType = 'dmgr'
{% endif %}

# which SSLSettings needed to be processed
{% if aliasSSLSettings is defined %}
aliasSSLSettings = '{{ aliasSSLSettings }}'
{% else %}
aliasSSLSettings = 'CellDefaultSSLSettings'
{% endif %}

# End - Input variables

# Loading the helper functions
{% include "wasHelper.j2.py" %}
# End - Loading the helper functions

def parseCertificates( rawIn ):
  result = []
  raworg = ""
  raworg = rawIn
  # to be able to split the lines... single quotes are needed instead of double..
  raworg.replace( '"', '\'' )
  for raw in raworg.split('\n'):
    item = parseString( raw )
    result.append( item )
  return result

def listCurrentCert(sslConfigDetails):
#  print 'Fetching the current certificaten for %s' % scopeType
  import re
  selfsignedsearchstr = 'CN=%s' % hostName
  attrs = '['
  attrs += '-keyStoreName  %s ' % sslConfigDetails['keyStore']
  attrs += '-keyStoreScope %s ]' % getScopeType()
  certString = AdminTask.listPersonalCertificates(attrs)
  certList = parseCertificates( certString )
  arrayItemList = []
  for currentCert in certList:
    arrayItem = {}
    arrayItem['cert'] = currentCert
    arrayItem['aabca'] = 'No'
    arrayItem['default'] = 0
    arrayItem['selfsigned'] = 'False'
    arrayItem['expireOn'] = checkValidity(currentCert['validity'])
    if currentCert['issuedBy'] == 'C=NL, L=Amsterdam, O=ABN AMRO Bank N.V., OU=ABN AMRO CISO, CN=ABN AMRO Bank Infra CA G2 ET':
       arrayItem['aabca'] = 'ET'
    if currentCert['issuedBy'] == 'C=NL, L=Amsterdam, O=ABN AMRO Bank N.V., OU=ABN AMRO CISO, CN=ABN AMRO Bank Infra CA G2':
       arrayItem['aabca'] = 'PR'
    if re.search(selfsignedsearchstr,currentCert['issuedBy']):
       arrayItem['selfsigned'] = 'True'
    if sslConfigDetails['default']==currentCert['alias']:
       arrayItem['default'] = 1 
    arrayItemList.append(arrayItem)
  return arrayItemList
 
def checkValidity(inputString):
  import re
  #from datetime import timedelta
  #from datetime import datetime

  #mininumeValidTo = datetime.now().date() + timedelta(days=mininumeValidDays)
  format_string = 'Valid from (.*) to (.*)\.'
  pattern = re.compile(format_string)
  parsed = pattern.match(inputString)
  #currently we are not intressed in the validFrom
  #validFrom = datetime.datetime.strptime(parsed.group(1),'%b %d, %Y').date()
  #validTo = datetime.strptime(parsed.group(2),'%b %d, %Y').date()
  #print parsed.groups()
  #print parsed.group(1)
  #print parsed.group(2)
  return parsed.group(2)

def infoCurrent(certList):
  currentCertsOut = {}
  for currentCert in certList:
    certItem = {}
    certItem['alias'] = currentCert['cert']['alias']
#    certItem['issuedBy'] = currentCert['cert']['issuedBy']
    certItem['expireOn'] = currentCert['expireOn']
    certItem['selfsigned'] = currentCert['selfsigned']
    certItem['fingerprint'] = 'SHA1 Fingerprint=' + currentCert['cert']['fingerPrint']
    default = 'False'
    if currentCert['default']:
      default = 'True'
    else:
      default = 'False'
    certItem['default'] = default
    certItem['aabca'] = currentCert['aabca'] 
    certItem['validityDays'] = -1
    certItem['certificate'] = currentCert['cert']
    currentCertsOut[certItem['alias']] = certItem
  return currentCertsOut

def extractSSlConfig(sslConfigDetails,searchStr):
  find_str_len=len(searchStr)
  start_find=sslConfigDetails.find(searchStr)+find_str_len +1
  j=sslConfigDetails[start_find:].find("]")
  return sslConfigDetails[start_find:start_find+j]

def unRawSSLConfig(instring):
  searchStr='('
  start_find=instring.find(searchStr)
  return instring[0:start_find]
  
def parseSSLConfig(sslConfigDetails):
  sslConfigOut={}
  sslConfigOut['default']   =extractSSlConfig( sslConfigDetails, "[serverKeyAlias")
  sslConfigOut['alias']   =extractSSlConfig( sslConfigDetails, "[alias")
  sslConfigOut['raw']={}
  sslConfigOut['raw']['keyStore']   =extractSSlConfig( sslConfigDetails, "[keyStore")
  sslConfigOut['raw']['trustStore'] =extractSSlConfig( sslConfigDetails, "[trustStore")
  sslConfigOut['keyStore']          =unRawSSLConfig(sslConfigOut['raw']['keyStore'])
  sslConfigOut['trustStore']        =unRawSSLConfig(sslConfigOut['raw']['trustStore'])

  return sslConfigOut
def getSSLConfig():
  attrs = '['
  attrs += '-alias  %s ' % aliasSSLSettings
  attrs += '-scopeName %s ]' % getScopeType()
  sslConfigDetails = AdminTask.getSSLConfig( attrs )
  return parseSSLConfig(sslConfigDetails)

scriptReturnMsg = {}
scriptReturnMsg['returncode'] = 0
try:
  scriptReturnMsg['sslconfig']=getSSLConfig()
  currentCertList = listCurrentCert(scriptReturnMsg['sslconfig'])
  
  scriptReturnMsg['currentcertificates']=infoCurrent(currentCertList)
  # communicate via std out to the calling module   
  print scriptReturnMsg

except AdminException, msg:
  print 'ERROR: failed to create the CSR %s / %s : %s' % (scopeType,hostName,msg)
  sys.exit(102)
