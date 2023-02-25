#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
from .regExpresser import get_name, dumper
from omc import encolored


def gather_files(path, exclude):
    _ret = {}
    if type(exclude) != str:
        exit('check regexp in Exclude:region.')
    for file in os.listdir(path):
        if os.path.isfile(path+'/'+file) and file[0] != '.':
            with open(path+'/'+file, 'r') as f:
                try:
                    _ret.update(get_name(f))
                except TypeError:
                    encolored.Error('Unformatted:', file)
                    exit()
    # Dict can't be motified during iteration, so change it to list.
    for name in list(_ret):
        if re.search(exclude, name, re.IGNORECASE):
            del _ret[name]
    return _ret


def processor(path, out="", exclude='限速|游戏|game'):
    emoji = 'template/emoji.txt'
    if out == "":
        out = path+'/region/'  # Shouldnt be same as path, make duplication.
    os.makedirs(out, exist_ok=True)
    parsed = open(emoji).read()
    re_list = parsed.strip().split('\n')
    proxies_dict = gather_files(path, exclude)
    # make a list of each region proxies and put them in for better flexbility.
    for num, re_ in list(enumerate(re_list)):
        re_match = re_.split(',')[0]
        re_emoji = re_.split(',')[1]
        encolored.Debug('Checking: ', re_emoji)
        locals()[f'list_{num}'] = []
        list_reg = locals()[f"list_{num}"]
        for proxies, line in list(proxies_dict.items()):
            if re.search(re_match, proxies):
                encolored.Info('\tMatched: ', proxies)
                list_reg.append(line)
                # solve duplicate match (China regexp.)
                del proxies_dict[proxies]
        if len(list_reg) != 0:
            with open(out + re_emoji, 'w') as f:
                dumper(list_reg, f)
