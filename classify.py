#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re,sys,os
syx="\d*\.*\d+(?:x|X|倍|倍率)"
file_path=sys.argv[1]
out=[]
print("processing: ",file_path)
if os.path.isdir(file_path+'_'):
    for root,dirs,files in os.walk(file_path+'_'):
        for file in files:
            os.remove(os.path.join(root,file))
        for dirc in dirs:
            os.remove(os.path.join(root,dirc))
with open(file_path) as file:
    f=(file.read())
    file_name = file_path.split('/')[-1]
    if re.search(syx,f):
        matches=(re.finditer(syx,f))
        for obj in matches:
            obj=obj.group()
            if not obj in out:
                os.makedirs(file_path + '_',exist_ok=True)
                with open(f"{file_path}_/{file_name}_{obj}","w+") as output:
                    lines=re.findall(".*\[{}\].*".format(obj),f)
                    all_lines=""
                    for line in lines: 
                        if all_lines=="": all_lines=line
                        else: all_lines+="\n"+line
                        f=f.replace("\n"+line,"")
                        f=f.replace(line,"")
                    output.write("proxies:\n"+all_lines)
                out+=[obj]
        with open(f"{file_path}_/{file_name}_plain","w+") as plain:
            plain.write(f)
        print(out)
    else: print("pattern cannot be matched.")