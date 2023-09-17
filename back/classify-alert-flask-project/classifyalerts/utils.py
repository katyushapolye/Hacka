
#problema de segunda ordem

#condições iniciais

#note que, o codigo esta todo modificado pra gerar graficos diferentes

from cProfile import label
import pandas as pd
from datetime import datetime
import json



#Dicionário de conversão de código de regra para ameaça

#Modify these for differing theats= kee=vek
threat_index = {
    "3CORESec": 1,
    "ACTIVEX": 1,
    "ADWARE_PUP": 1,
    "ATTACK_RESPONSE": 1,
    "BOTCC_(BOT_COMMAND_AND_CONTROL)": 1,
    "BOTCC_PORTGROUPED": 1,
    "CHAT": 1,
    "CIARMY": 1,
    "COINMINER": 1000,
    "COMPROMISED": 1,
    "CURRENT_EVENTS": 1,
    "DELETED": 1,
    "DNS": 1,
    "DOS": 1,
    "DROP": 1,
    "DSHIELD": 1,
    "EXPLOIT": 1000,
    "EXPLOIT-KIT": 1000,
    "FTP": 1,
    "GAMES": 0,
    "HUNTING": 1,
    "ICMP": 1,
    "ICMP_INFO": 0,
    "IMAP": 1,
    "INAPPROPRIATE": 1,
    "INFO": 0,
    "JA3": 1000,
    "MALWARE": 1000,
    "MISC.": 1,
    "MOBILE_MALWARE": 1000,
    "NETBIOS": 1,
    "P2P": 1,
    "PHISHING": 500,
    "POLICY": 1,
    "POP3": 1,
    "RPC": 1,
    "SCADA": 1,
    "SCADA_SPECIAL": 1,
    "SCAN": 1,
    "SHELLCODE": 1,
    "SMTP": 1,
    "SNMP": 1,
    "SQL": 500,
    "TELNET": 1,
    "TFTP": 1,
    "TOR": 0,
    "TROJAN": 1000,
    "Threatview.io": 1,
    "USER_AGENTS": 1,
    "VOIP": 1,
    "WEB_CLIENT": 1,
    "WEB_SERVER": 1,
    "WEB_SPECIFIC_APPS": 1,
    "WORM": 1
}

pops = [
    'Terra.json',
    'Jupyter.json',
]

pops_dict = {
    'Terra': 0,
    'Jupyter': 1 
}

classifications = {
    #Name, lowerbound upperbound - > [inclusive in the entry and exclusive in the exit)
    (0,10):'Minor',
    (10,20):'Mild',
    (20,50):'Major',
    (50,5000):'Severe',
    (5000,80000):'Critical',
    (80000,9999999):'Catastrophic'
    
}

#IP -> (threatLevel,lastTimeStamp)
threat_control = {
    
}

from datetime import datetime


def parseThreat(threatString):
    split =  threatString.split(" ")
    firstKey = split[1]
    secondKey = split[2]
    thirdKey = split[3]

    
    #Casos Individuais botcc
    if firstKey == 'Botcc':
        if(secondKey == 'Portgrouped'):
            return (firstKey + ' ' + secondKey)
        else:
            #returns the whole other string
            return "Botcc (Bot Command and Control)"

    #web   
    if firstKey == 'Web':
        if(thirdKey == 'Apps'):
            return "Web Specific Apps"
        return ('Web ' + secondKey)
    
    if firstKey == 'User':
        return 'User Agents'
    
    if firstKey == 'Mobile':
        return 'Mobile Malware'
    
    if firstKey == 'Current':
        return 'Current Events'

    return firstKey
    
        


def classifyThreatLevel(level):

    for key,value in classifications.items():
        if(level in range(key[0],key[1])):
            return value

def UpdateIP(ip, threat, timestamp):
    if ip not in threat_control:
        newvalue = (threat_index[threat], timestamp)
        threat_control[ip] = newvalue
    else:
        existing_value = threat_control[ip]
        existing_timestamp = datetime.strptime(existing_value[1], "%Y-%m-%d %H:%M:%S")
        new_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        
        # Check if the timestamps are more than 8 hours apart
        if (new_timestamp - existing_timestamp).total_seconds() > 8 * 3600:
            newvalue = (0 + threat_index[threat], timestamp)
        else:
        
            newvalue = (existing_value[0] + threat_index[threat], timestamp)
        
        threat_control[ip] = newvalue


dfs = []
dfnews = []

for p in pops:
    json_file_path = p

    with open(json_file_path, 'r', encoding='utf-8') as file:
        try:
            json_data = json.load(file)
            # If successful, the JSON is valid
            print("JSON is valid.")
        except json.JSONDecodeError as e:
            print("JSON is not valid:", e)

    df = pd.read_json(json_file_path,encoding='utf-8')
    dfs.append(df)
    dfnew = df[['timestamp', 'dest_ip','dest_port','src_ip','src_port','alert.severity','alert.signature','alert.category','alert.suricata_id']]  # Replace 'A' and 'C' with the column names you want
    #print(df.head())



    threat_list = []
    classification_list = []


    for index, row in dfnew.iterrows():
        timestamp = row['timestamp']
        ipSRC = row['src_ip']
        ipDST = row['dest_ip']    
        rule =  row['alert.signature'] #turn into threat_index
        #threat_level = row['threat_level']
        #print("ALERT.SIG: {}".format(rule))
        #Raise threat level, as of now, for both the src and dest IP equally
        UpdateIP(ipSRC,parseThreat(rule),str(timestamp))
        UpdateIP(ipDST,parseThreat(rule),str(timestamp))
        threat_level = int((threat_control[ipSRC][0] + threat_control[ipDST][0])/2)
        threat_list.append(threat_level)
        classification_list.append(classifyThreatLevel(threat_level))



    dfnew['threat_level'] = threat_list
    dfnew['class'] = classification_list
    threat_control = dict(sorted(threat_control.items(), key=lambda item: item[1][0],reverse=True))    

    #filtered_df = df[df['src_ip'].str.contains('b963fb6146d046d6e64ce6bfa266dddff2dded02a822b7f94bf92e61f04d5cca', case=False, regex=False)]
    print(dfnew.head())
    dfnew = dfnew.sort_values(by = 'threat_level',ascending=False)
    dfnews.append(dfnew)
    #dfnew.to_csv('newClass.csv',index=False)




#csv_output_path = 'terradump.csv'

# Save the DataFrame to a CSV file  
#df.to_csv(csv_output_path, index=False)


threat_count = {
    "3CORESec": 0,
    "ACTIVEX": 0,
    "ADWARE_PUP": 0,
    "ATTACK_RESPONSE": 0,
    "BOTCC_(BOT_COMMAND_AND_CONTROL)": 0,
    "BOTCC_PORTGROUPED": 0,
    "CHAT": 0,
    "CIARMY": 0,
    "COINMINER": 0,
    "COMPROMISED": 0,
    "CURRENT_EVENTS": 0,
    "DELETED": 0,
    "DNS": 0,
    "DOS": 0,
    "DROP": 0,
    "DSHIELD": 0,
    "EXPLOIT": 0,
    "EXPLOIT-KIT": 0,
    "FTP": 0,
    "GAMES": 0,
    "HUNTING": 0,
    "ICMP": 0,
    "ICMP_INFO": 0,
    "IMAP": 0,
    "INAPPROPRIATE": 0,
    "INFO": 0,
    "JA3": 0,
    "MALWARE": 0,
    "MISC.": 0,
    "MOBILE_MALWARE": 0,
    "NETBIOS": 0,
    "P2P": 0,
    "PHISHING": 0,
    "POLICY": 0,
    "POP3": 0,
    "RPC": 0,
    "SCADA": 0,
    "SCADA_SPECIAL": 0,
    "SCAN": 0,
    "SHELLCODE": 0,
    "SMTP": 0,
    "SNMP": 0,
    "SQL": 0,
    "TELNET": 0,
    "TFTP": 0,
    "TOR": 0,
    "TROJAN": 0,
    "Threatview.io": 0,
    "USER_AGENTS": 0,
    "VOIP": 0,
    "WEB_CLIENT": 0,
    "WEB_SERVER": 0,
    "WEB_SPECIFIC_APPS": 0,
    "WORM": 0
}
# FUNCTIONS 

def topAmeacas(region, date, pop):

    if region == 'CAIS':
        df_used = pd.concat([dfnews[0], dfnews[1]], ignore_index=True)
    if region == 'PoP':
        ind = pops_dict[pop] 
        df_used = dfnews[ind]
    

    for index, row in df_used.iterrows():   
        rule =  row['alert.signature'] #turn into threat_index
        treat =  parseThreat(rule)
        threat_count[treat] = threat_count[treat] + 1
    

    return threat_count

def fillTableClass(region, pop):
    if region == 'CAIS':
        df_used = pd.concat([dfnews[0], dfnews[1]], ignore_index=True)
    if region == 'PoP':
        ind = pops_dict[pop] 
        df_used = dfnews[ind]

    matrix = []
    for index, row in df_used.iterrows():
        line = []   
        rule =  row['alert.signature'] #turn into threat_index
        treat =  parseThreat(rule)
        ipSRC = row['src_ip']
        ipDST = row['dest_ip'] 
        portDST = row['dest_port']
        portSRC = row['src_port']    
        tclass = row['class']
        line.append(ipSRC)
        line.append(ipDST)
        line.append(portDST)
        line.append(portSRC)
        line.append(tclass)
        line.append(treat)

        matrix.append(line)

    return matrix
