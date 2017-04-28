import requests
import ipgetter

username = "[USERNAME]"
token = "[TOKEN]"
host = "[A-RECORD]"
domain = ".[DOMAINNAME]"
ipaddr = ipgetter.myip()


#Check if IP has changed
#If changed get record_id of hostname
#delete hostname by record_id
#create new record with new IP

def createHost(host, ipaddr):
    url = "https://api.name.com/api/dns/create/packetsquirrel.net"

    payload = "{\n\t\"hostname\" : \"" +host+ "\",\n\t\"type\" : \"A\",\n\t\"content\" : \"" +ipaddr+ "\",\n\t\"ttl\" : 300\n}"

    headers = {
        'api-username': username,
        'api_token': token,
        'content-type': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

def getHostRecord(name, key):
    url = "https://api.name.com/api/dns/list/packetsquirrel.net"

    headers = {
        'api-username': username,
        'api-token': token,
        'content-type': "application/json"
    }

    response = requests.request("GET", url, headers=headers)
    r_json = response.json()
#rjson 'records' is a list of dictionaries, each dictionary reprents a hostname and its key/values - print r_json['records'][1]['name']

#search each dictionary for the name we want and return the record
    for dicts in r_json['records']:
        if dicts['name'] == name:
            #print dicts['record_id']
            return dicts[key]

def deleteHost(recordID):
    url = "https://api.name.com/api/dns/delete/packetsquirrel.net"

    payload = "{\n\t\"record_id\" : " + str(recordID) + "\n}"
    headers = {
        'api-username': username,
        'api_token': token,
        'content-type': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

def checkIP():
    if ipaddr != getHostRecord(host+domain, 'content'):
        hostrecord = getHostRecord(host+domain, 'record_id')
        deleteHost(hostrecord)
        createHost(host, ipaddr)
        print "Update Completed!", host+domain, "has been updated with", ipaddr, "."
    else:
        print "No need to update,", ipaddr, "is already synchronized with", host+domain, "."

checkIP()
