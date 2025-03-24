# .fconfig File Parser v1.2
# Created by Patrick G. Karhoff [Github: Patric-k-k]

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
                        elif WANTEDtype == "list":
                            seperated = Data.split(",")
                            for i in seperated:
                                seperated[seperated.index(i)] = i.strip()
                            return seperated
                        elif WANTEDtype == "klist":
                            seperated = Data.split(",")
                            return seperated
                        else:
                            raise TypeError(f"Type {WANTEDtype} not supported")
                    except ValueError:
                        print(f"Could not convert {Data} to {WANTEDtype}. Invalid config. Key: {key}. Line: {Rawdata.index(OriginalData)+1}")
                        if die_on_error:
                            exit(78)
                        else:
                            return None
    raise KeyError # Couldn't find the key
def save_data(key,file,data,die_on_error=True):
    with open(file, 'r') as f:
        Fdata = f.readlines()
    for i in Fdata:
        Processed = i.split("|")
        if Processed[0] == key:
            try:
                Full_data_section = Processed[len(Processed)-1]
                comment = Full_data_section.split("<")[0]
                if len(Full_data_section)-1 == 1:
                    raise Exception("Invalid config file (No data)")
                if len(Processed)-1 == 1:
                    Fdata[Fdata.index(i)] = f"{Processed[0]}|{comment}<{data}>"
                elif len(Processed)-1 == 2:
                    Fdata[Fdata.index(i)] = f"{Processed[0]}|{Processed[1]}|{comment}<{data}>"
                else:
                    if die_on_error == True:
                        raise Exception(f"Invalid config file (len: {len(Processed)})")
                    else:
                        return Exception(f"Invalid config file (len: {len(Processed)})")
            except Exception as err:
                if die_on_error == True:
                    raise err
                else:
                    return err
    #make SURE that lines get seperated.
    for i in Fdata:
        Fdata[Fdata.index(i)] = Fdata[Fdata.index(i)] + "\n"
    #make lists work
    for i in Fdata:
        if len(i.split("|")) > 1:
            Key = i.split("|")[0]
            Dtype = i.split("|")[1].lower()
            if i.split("|")[1].lower() == "list" or i.split("|")[1].lower() == "klist":
                e = i.split("|")[2].replace("'","").replace("[","").replace("]","")
                Fdata[Fdata.index(i)] = f"{Key}|{Dtype}|{e}"
    #remove blank lines
    for i in Fdata:
        if Fdata[Fdata.index(i)] == "\n" or Fdata[Fdata.index(i)] == "\n\n":
            Fdata.remove(i)
    print(Fdata)
    with open(file, 'w+') as f:
        f.writelines(Fdata)
