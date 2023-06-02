# Input variables for the wasHelper
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
# End - Input variables
def getScopeType():
  keyStoreScope = '(cell):%s-cell' % hostName
  if scopeType == 'node':
    keyStoreScope= keyStoreScope+':(node):%s-node' % hostName
  return keyStoreScope


def getstorePrefix():
  storePrefix = 'Cell'
  if scopeType == 'node':
    storePrefix = 'Node'
  return storePrefix

# This is not the most elegant implementation... But has to do for now
# Rework is most adviced
def parseString( inputString ):
  localString = ''
  localString = inputString
  nextLevel = ''
  result = {}
  #print 'localString: --- ' + localString + ' ---'
  #strip off all whitespaces
  # [[a.[bb]].[c.d].[e.f]<>.[x.[yyyy]].]
  localString = localString.strip()
  # outer bracked have to go....
  localString = localString[1:-2]
  # [a.[bb]].[c.d].[e.f]<>.[x.[yyyy]].
  #strip off all whitespaces
  localString = localString.strip()
  # [a.[bb]].[c.d].[e.f]<>.[x.[yyyy]]
  localString = localString[1:-1]
  # outer bracked have to go....
  # a.[bb]].[c.d].[e.f]<>.[x.[yyyy]
  #strip off all whitespaces
  # make it a list....
  localString = localString.replace( "] [", "],[" )
  # a.[bb]],[c.d],[e.f]<>,[x.[yyyy]
  outterList = localString.split("],[")
  # the string is now split up ... the item between the brackes are part of the same key..
  # a.[bb]
  # c.d
  # e.f
  # <>
  # x.[yyyy]
  for o in outterList:
    #make each variable into a key:value
    #strip off the square brackets that surround each key:value pair
    str = o.strip()
    splitChar = ' '
    if str[-1] == ']':
      splitChar = '['
    #separate the key from the value
    lst = str.split( splitChar, 1)
    # and add it to our master List
    # always trim the spaces....
    # and remove the closing bracket
    lstvar = lst[1].strip()
    if lstvar[-1] == ']':
      lstvar = lstvar[:-1]
    result[ lst[0].strip() ]  =  lstvar
  #endfor
  return result
