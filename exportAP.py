import sys, csv, os
import requests, json, urllib3, time
import argparse
from datetime import datetime

urllib3.disable_warnings()

prime_server = 'http://prime.domain.com' #prime url
prime_user = 'user_read' #prime user with read permissions
prime_passwd = 'user_passwd' #prime user passwd

# defs
def ap_search(apName): # search for ap
    uri = prime_server + '/webacs/api/v1/data/AccessPoints.json?name="{}"'.format(apName)
    r = requests.get(uri, headers={'Connection':'close'}, auth=(prime_user, prime_passwd), timeout=100, verify=False)
    time.sleep(0.5) #'message': 'NBI Rate limit for user (user_read) exceeded (More than 5 in 1,000 ms).-PRS-303'
    return(r.json()['queryResponse'])

def get_apdata(url): # get ap data
    r = requests.get(url + '.json', headers={'Connection':'close'}, auth=(prime_user, prime_passwd), timeout=100, verify=False)
    time.sleep(0.5) #'message': 'NBI Rate limit for user (user_read) exceeded (More than 5 in 1,000 ms).-PRS-303'
    return(r.json()['queryResponse'])

def format_aplist(list): # format the list
    f = open(list)
    aps = csv.reader(f)
    aplist = []
    for ap in aps:
      aplist.append(ap[0])
    return(aplist)

def format_apdata(data): # data to fetch
    datalist = []
    serialNumber = data['entity'][0]['accessPointsDTO']['serialNumber']
    name = data['entity'][0]['accessPointsDTO']['name']
    model = data['entity'][0]['accessPointsDTO']['model']
    ethernetMac = data['entity'][0]['accessPointsDTO']['ethernetMac']
    datalist.append(serialNumber)
    datalist.append(name)
    datalist.append("AP")
    datalist.append("AP")
    datalist.append("Cisco")
    datalist.append(model)
    datalist.append(ethernetMac)
    # custom data goes below, edit if needed
    # nilex_konto = ''
    # nilex_pris = ''
    # nilex_manadskostnad = ''
    # nilex_avskrivtid = ''
    # nilex_intakt_ansvar = ''
    # nilex_intakt_konto = ''
    # nilex_intakt_projekt = ''
    # nilex_intakt_verksamhet = ''
    # datalist.append(nilex_konto)
    # datalist.append(nilex_pris)
    # datalist.append(nilex_manadskostnad)
    # datalist.append(nilex_avskrivtid)
    # datalist.append(nilex_intakt_ansvar)
    # datalist.append(nilex_intakt_konto)
    # datalist.append(nilex_intakt_projekt)
    # datalist.append(nilex_intakt_verksamhet)
    print(datalist)
    return(datalist)

def export_csv(data):
    d_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    csv_output = 'output_{}.csv'.format(d_now)
    print("Exporting csv...")
    with open(csv_output, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(data)
    print("Done, exported csv: "+os.getcwd()+"/{}".format(csv_output))

if __name__ == '__main__':
    #args
    parser = argparse.ArgumentParser()
    parser.add_argument('--aplist', action='store')
    args = parser.parse_args()
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    aplist = args.aplist

    #exportAP.py start
    aps = format_aplist(aplist)
    export_list = []
    for ap in aps:
        ap_searchdata = ap_search(ap)
        if ap_searchdata['@count'] == '1':
            for data in ap_searchdata['entityId']:
                ap_url = data['@url']
                ap_data = get_apdata(ap_url)
                ap_data_format = format_apdata(ap_data)
                export_list.append(ap_data_format)
        else:
            print("['{} not found in Prime!']".format(ap))
            notfound = ["{} not found in Prime!".format(ap)]
            export_list.append(notfound)

    export_csv(export_list) #export list of lists
