# .fconfig File Parser v1.0
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

def read_data(key,file,die_on_error = True):
    with open(file,'r') as f:
        Rawdata = f.readlines()
    for i in Rawdata:
        OriginalData = i
        i = i + "|"
        if i[0] != "#":
            i.strip("\n")
            i = i.split("|")
            if i[0] == key:
                if i[2] == "":
                    i = i[1].split('<')
                    i = i[1]
                    i = i.split('>')
                    i = i[0]
                    return to_data_type(i)
                else:
                    WANTEDtype = i[1].lower()
                    Data = i[2]
                    Data = Data.split('<')
                    Data = Data[1]
                    Data = Data.split('>')
                    Data = Data[0]
                    try:
                        if WANTEDtype == "int":
                            return int(Data)
                        elif WANTEDtype == "float":
                            return float(Data)
                        elif WANTEDtype == "bool":
                            return Data.lower() == "true"
                        elif WANTEDtype == "str":
                            return Data
                        else:
                            raise TypeError(f"Type {WANTEDtype} not supported")
                    except ValueError:
                        print(f"Could not convert {Data} to {WANTEDtype}. Invalid config. Key: {key}. Line: {Rawdata.index(OriginalData)+1}")
                        if die_on_error:
                            exit(78)
                        else:
                            return None
    raise KeyError # Couldn't find the key
