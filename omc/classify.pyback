#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re,os
def run(syx, file_path):
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
        file_lines = f.split('\n')
        if re.search(syx,f):
            matches = re.finditer(syx,f)
            all_matched_set = set()
            for obj in matches:
                obj=obj.group()
                if not obj in out:
                    os.makedirs(file_path + '_',exist_ok=True)
                    lines = re.findall(".*{}.*".format(obj),f)
                    all_matched_set = all_matched_set | set(lines)
                    txt = ""
                    for line in lines: 
                        txt += line+'\n'
                    with open(f"{file_path}_/{file_name}_{obj}","w+") as output:
                        if txt.strip() != "": output.write("proxies:\n"+txt)
                    out += [obj] # New method!
            left_set = set(file_lines) - all_matched_set
            if "proxies:" in left_set:
                if len(left_set) == 1: print('All matched, no _plain will be created.')
                else:
                    left_set.remove('proxies:') # 'proxies:' may not be on the first line, so remove it and add it later.
                    with open(f"{file_path}_/{file_name}_plain","w+") as plain:
                            plain.write('proxies:\n' + "\n".join(left_set)) # New method! str.join(<str>)
            else: print("'proxies:' not found, check the proceeded file.")
            print("Matched: ", out)
            file.close()
            _file_All = file_path+'_All'
            if os.path.exists(_file_All): os.remove(_file_All)
            os.rename(file_path,_file_All)
        else: 
            print("pattern cannot be matched.")
