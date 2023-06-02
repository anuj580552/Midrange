"""Jinja2 template to generate the jython script.

The extension of this file has been choosen to be py... This will enable 
the suported editing tools for python.

The Global variables are passed by the calling module.
"""
import sys
from com.ibm.websphere.management.exception import AdminException

# End - Global variable 




# Input variables passed by call script
{% if inventory_hostname is defined %}
# setup hostname
hostName = '{{ inventory_hostname }}'
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

{% if currentDefault is defined %}
# setup currentDefault
currentDefault = '{{ currentDefault }}'
{% else %}
# currentDefault is not defined... assume default
currentDefault = 'default'
{% endif %}
{% if newDefault is defined %}
# setup currentDefault
newDefault = '{{ newDefault }}'
{% else %}
# currentDefault is not defined... assume nothing...
newDefault = '----'
{% endif %}
# End - Input variables
{% if sslConfig is defined %}
# setup currentDefault
sslConfig = {{ sslConfig }}
{% else %}
# currentDefault is not defined... assume nothing...
sslConfig = None
{% endif %}
{% include "wasHelper.j2.py" %}



def activateNewDefault( currentDefault , newDefault ):
  attrs = '['
  attrs += '-certificateAlias %s ' % currentDefault
  attrs += '-replacementCertificateAlias %s ' % newDefault
  attrs += '-deleteOldCert true ' 
  attrs += '-deleteOldSigners false '
  attrs += '-keyStoreName  %s ' % sslConfig['keyStore']
  attrs += '-keyStoreScope %s ]' % getScopeType()
  print attrs
  AdminTask.replaceCertificate(attrs) 
  AdminConfig.save()

activateNewDefault ( currentDefault , newDefault )