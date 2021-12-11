#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re,sys
syx="\d*\.*\d+(?:x|X|倍|倍率)"
file_path=sys.argv[1]
out=[]
print("processing: ",file_path)
with open(file_path) as file:
    f=(file.read())
    if re.search(syx,f):
        matches=(re.finditer(syx,f))
        for obj in matches:
            obj=obj.group()
            if not obj in out:
                with open(f"{file_path}_{obj}","w+") as output:
                    lines=re.findall(".*\[{}\].*".format(obj),f)
                    all_lines=""
                    for line in lines: 
                        if all_lines=="": all_lines=line
                        else: all_lines+="\n"+line
                        f=f.replace("\n"+line,"")
                        f=f.replace(line,"")
                    output.write("proxies:\n"+all_lines)
                out+=[obj]
        with open(file_path+"_plain","w+") as plain:
            plain.write(f)
        print(out)
    else: print("pattern cannot be matched.")