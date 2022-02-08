#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
import requests
from .classify import get_name, dumper


def gather_files(path, exclude):
    _ret = {}
    if type(exclude) != str:
        exit('check regexp in Exclude:region.')
    for file in os.listdir(path):
        if os.path.isfile(path+'/'+file):
            with open(path+'/'+file, 'r') as f:
                _ret.update(get_name(f))
    # Dict can't be motified during iteration, so change it to list.
    for name in list(_ret):
        if re.search(exclude, name, re.IGNORECASE):
            del _ret[name]
    return _ret


def processor(path, out="", exclude='限速|游戏|game'):
    if out == "":
        out = path+'/region/'  # Shouldnt be same as path, make duplication.
    os.makedirs(out, exist_ok=True)
    parsed = requests.get('https://raw.githubusercontent.com/tindy2013/subconverter/master/base/snippets/emoji.txt',
                          allow_redirects=True).content.decode('utf-8')
    re_list = parsed.strip().split('\n')
    proxies_dict = gather_files(path, exclude)
    # make a list of each region proxies and put them in for better flexbility.
    for num, re_ in list(enumerate(re_list)):
        re_match = re_.split(',')[0]
        re_emoji = re_.split(',')[1]
        print('Regexp: ', re_emoji)
        locals()[f'list_{num}'] = []
        # use local() func mannally, otherwise would be recognize as str. because var is spliced by string.format.
        list_reg = locals()[f"list_{num}"]
        for proxies, line in list(proxies_dict.items()):
            if re.search(re_match, proxies):
                print('\tMatched: ', proxies)
                list_reg.append(line)
                # solve duplicate match (China regexp.)
                del proxies_dict[proxies]
        if len(list_reg) != 0:
            with open(out + re_emoji, 'w') as f:
                dumper(list_reg, f)
