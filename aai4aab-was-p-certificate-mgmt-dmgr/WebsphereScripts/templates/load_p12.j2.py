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

{% if p12StorePath is defined %}
p12StorePath = '{{ p12StorePath }}'
{% else %}
p12StorePath = 'errorpath'
{% endif %}

{% if p12StorePasswd is defined %}
p12StorePasswd = '{{ p12StorePasswd }}'
{% else %}
p12StorePasswd = ''
{% endif %}

{% if certificateAlias is defined %}
certificateAlias = '{{ certificateAlias }}'
{% else %}
certificateAlias = 'default-{{ scopeType }}'
{% endif %}

{% if trustAlias is defined %}
trustAlias = '{{ trustAlias }}'
{% else %}
trustAlias = 'root-ca-{{ scopeType }}'
{% endif %}
{% if sslConfig is defined %}
# setup currentDefault
sslConfig = {{ sslConfig }}
{% else %}
# currentDefault is not defined... assume nothing...
sslConfig = '----'
{% endif %}
# End - Input variables

{% include "wasHelper.j2.py" %}

def getP12KeystoreAliases():
  attrs = '['
  attrs += '-keyFilePath %s ' % p12StorePath 
  attrs += '-keyFilePassword %s ' % p12StorePasswd
  attrs += '-keyFileType PKCS12 '
  attrs += ' ]' 
  aliases = AdminTask.listKeyFileAliases(attrs) 
  return aliases
  
def loadP12Keystore(aliasP12,alias):
  attrs = '['
  attrs += '-keyFilePath %s ' % p12StorePath 
  attrs += '-keyFilePassword %s ' % p12StorePasswd
  attrs += '-keyFileType PKCS12 '
  attrs += '-certificateAliasFromKeyFile %s ' % aliasP12
  attrs += '-certificateAlias %s ' % alias
  attrs += '-keyStoreName  %s ' % sslConfig['keyStore']
  attrs += '-keyStoreScope %s ]' % getScopeType()
  AdminTask.importCertificate(attrs) 

def loadPEMTruststore(alias):
  attrs = '['
  attrs += '-certificateFilePath %s ' % pemStorePath 
  attrs += '-base64Encoded true '
  attrs += '-certificateAlias %s ' % alias
  attrs += '-keyStoreName  %s ' % sslConfig['trustStore']
  attrs += '-keyStoreScope %s ]' % getScopeType()
  AdminTask.addSignerCertificate(attrs) 


aliasesP12 = getP12KeystoreAliases()
loadP12Keystore(aliasesP12,certificateAlias)
#loadPEMTruststore(trustAlias)
AdminConfig.save()