# .fconfig File Parser
# Created by Patrick G. Karhoff [Github: Patric-k-k, Email]

def to_data_type(data):
    if data.isdigit():
        return int(data)
    
    try:
        return float(data)
    except ValueError:
        pass

    if data.lower() in ["true","false"]:
        return data.lower() == "true"
    if data.lower() in ["yes","no"]:
        return data.lower() == "yes"
    
    return data

def read_data(key,file):
    with open(file,'r') as f:
        Rawdata = f.readlines()
    for i in Rawdata:
        if i[0] != "#":
            i.strip("\n")
            i = i.split("|")
            if i[0] == key:
                i = i[1].split('<')
                i = i[1]
                i = i.split('>')
                i = i[0]
                return to_data_type(i)
    raise KeyError # Couldn't find the key