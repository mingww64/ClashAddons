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
        all_lines=""
        for obj in matches:
            obj=obj.group()
            if not obj in out:
                with open(f"{file_path}_{obj}","w+") as output:
                    lines=re.findall(".*\[{}\].*".format(obj),f)
                    oline=""
                    for line in lines: 
                        if oline=="": oline=line
                        else: oline+="\n"+line
                        f=f.replace("\n"+line,"")
                        f=f.replace(line,"")
                    output.write(oline)
                    all_lines+=oline
                out+=[obj]
        with open(file_path+"_plain","w+") as plain:
            plain.write("proxies:\n"+f)
        print(out)
    else: print("pattern cannot be matched.")