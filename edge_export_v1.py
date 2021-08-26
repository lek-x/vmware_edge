import requests
import base64
import os
import sys
import time


edge_e = str()
x = str()
y = str()
z = str()
b = str()
api_e=str()
auth_header = str()
h=str()


if sys.platform == 'win32':
	clear = lambda: os.system('cls')
elif sys.platform == 'linux':
	clear = lambda: os.system('clear')

print('NSX Edge Settings Exporter (VMWare vDirector) v1.0 by Mezentsev Roman')
time.sleep(2)

clear()


########User's input section########

x = input('Enter API endpoint (e.g. vcd6.vdcportal.com): ')
y = input('Enter your login: ')
z = input('Enter your v_org (e.g. org_1344546): ')
b = input('Enter your pass: ')



#######Saved credentials
#Comment User's input section if you want to use saved credentials below
#x = 'vcd6.vdcportal.com'
#y = 'admin'
#z = 'org_1344546'
#b = 'password'

#############Get auth token################
def bs64(x,y,z,b):
    api_e = 'https://'+ x + '/api/sessions'
    h = (str(y)+'@'+str(z)+':' + str(b)).encode('utf-8')
    e = base64.b64encode(h)
    base_res=e.decode('utf-8')
    print('\n','It is your auth token>>: ',base_res)
    auth_header='Basic'+' ' + str(base_res)
    return (auth_header,api_e)
#################Request  vcloud access-token section##################
def vcltok(auth_header, api_e):
    endpoint = str(api_e)
    data = """<?xml version='1.0' encoding='utf-8'?>"""
    headers = {"Authorization": "Basic none", "Content-Type": 'application/json', "Accept": '*/*', "Accept": 'application/*+xml;version=33.0' }
    headers["Authorization"] = str(auth_header)
    response = requests.post(endpoint,data=data, headers=headers)
    br_token = response.headers['x-vmware-vcloud-access-token']
    print('\n','It is your Bearer Token>>: ',br_token)
    auth_header2='Bearer'+' ' + str(br_token)
    return auth_header2
########Finding Edge ID################################################
def edgeid(auth_header2):
    edge_e = 'https://'+ x + '/network/edges/'
    endpoint1 = str(edge_e)
    data1 = """<?xml version='1.0' encoding='utf-8'?>"""
    headers1 = {"Authorization": "Bearer none", "Content-Type": 'application/json', "Accept": '*/*', "Accept": 'application/*+xml;version=33.0' }
    headers1["Authorization"] = str(auth_header2)
    #print(headers1)
    response1 = requests.get(endpoint1,data=data1, headers=headers1)
    k = response1.text
    #print(k)
    fn1=k.find('<id>')
    fn2= k.find('</id>')
    fnr = fn2-fn1
    edge_id = k[fn1+4:fn2]
    print('\n',"Your NSX Edge ID>>>>: ",edge_id)
    return (edge_id, endpoint1)
###########Request Firewall rulles###############################
def fwrules(edge_id,endpoint1):
    endpoint2 = endpoint1+edge_id+'/firewall/config'
    data2 = """<?xml version='1.0' encoding='utf-8'?>"""
    headers2 = {"Authorization": "Bearer none", "Content-Type": 'application/json', "Accept": '*/*', "Accept": 'application/*+xml;version=33.0' }
    headers2["Authorization"] = str(auth_header2)
    response2 = requests.get(endpoint2,data=data2, headers=headers2)
    #print('\n')
    #print('Below your Firewall rules>>:','\n')
    rp2 = response2.text
    #print(response2.text)
    return rp2
###################Request NAT rulles#############################
def natrules(endpoint1,edge_id,auth_header2 ):
    endpoint3 = endpoint1+edge_id+'/nat/config'
    data3 = """<?xml version='1.0' encoding='utf-8'?>"""
    headers3 = {"Authorization": "Bearer none", "Content-Type": 'application/json', "Accept": '*/*', "Accept": 'application/*+xml;version=33.0' }
    headers3["Authorization"] = str(auth_header2)
    response3 = requests.get(endpoint3,data=data3, headers=headers3)
    #print('\n')
    #print('Below your NAT rules>>:','\n')
    rp3 = response3.text
    return rp3
    #print(response3.text)    
################Exporting Configs to files#####################
def export(rp2,rp3): 
     file = open(str('fw_rules_'+z+".xml"), "w")
     file.write(rp2)
     file.close()
     file = open(str('nat_rules_'+z+".xml"), "w")
     file.write(rp3)
     file.close()
     print('\n','Your config was exported in files>> ', str('fw_rules_'+z+".xml"), ',', str('nat_rules_'+z+".xml"))

######Main block###############################################
resb64=bs64(x,y,z,b)
auth_header = resb64[0]
api_e = resb64[1]
time.sleep(2)
resvcltok =vcltok(auth_header,api_e) 
auth_header2 =resvcltok[:]
time.sleep(2)
resedgeid=edgeid(auth_header2)

edge_id=resedgeid[0]
endpoint1=resedgeid[1]
time.sleep(2)
resfwrules=fwrules(edge_id,endpoint1)
rp2=resfwrules

resnatrules=natrules(endpoint1,edge_id,auth_header2)  
rp3=resnatrules

export(rp2,rp3)

input("\n Press any key to exit")
