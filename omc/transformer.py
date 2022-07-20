import os
import requests
import yaml
import re
from . import regExpresser


class Kit:
    '''use class to handle variables change, 
otherwise vars will init before giving new config_path, 
which cause undefined / no such file errors'''  # i can use function though...
    config_path = './omc/config.yaml'

    def __init__(self, path):
        if os.path.exists(path):
            if path != self.config_path:
                print("{} -> {}".format(self.config_path, path))
            self.__dict__['config_path'] = path
        elif os.path.exists(self.config_path):
            print(
                f'the given path: {path} is not exist, fallback to {self.config_path}')
        else:
            exit(f'{self.config_path} not found.')
        config = open(self.config_path, 'r').read()
        parse_conf = yaml.safe_load(config)
        if not parse_conf['Enabled']:
            exit(f'omc is Disabled in its config file: {self.config_path}.')
        self.subc = parse_conf['SCServer']
        self.subc_remote = parse_conf['SCServerRemote']
        self.head = parse_conf['Rules']['Clash']['head']
        self.rules = parse_conf['Rules']['Clash']['rules']
        self.parse_conf = parse_conf
        self.unavailable_providers = list()

    def check_if_available(self, content, typ, provider_name):
        # This counting method has a issue with single line files.
        num = len(re.findall('\n', content))

        def set_unavailable():
            self.unavailable_providers.append(provider_name)
            return False
        print(num, 'Lines')
        if num == 0 and typ == 'clash':
            return set_unavailable()
        if ' = ' not in content and ', ' not in content and num == 0 and typ == 'quanx':
            return set_unavailable()
        return True

    def get_providers(self, dir):
        def load_args(target, provider):
            if self.parse_conf.__contains__('Exclude Args'):
                ret = "exclude=false&"  # Disable exclude func
                if self.parse_conf['Exclude Args'].__contains__('syntax'):
                    ret = "exclude=" + \
                        self.parse_conf['Exclude Args']['syntax'] + '&'
                if self.parse_conf['Exclude Args'].__contains__('whitelist') and type(self.parse_conf['Exclude Args']['whitelist']) == list:
                    # disable exclude func for providers in whitelist
                    if provider in self.parse_conf['Exclude Args']['whitelist']:
                        ret = "exclude=false&"
            else:
                ret = ""  # exclude with subC default filters
            for key, value in self.parse_conf[target].items():
                ret += f'{key}={value}&'
            # convert boolean to str in url
            return ret.replace('True', 'true').replace('False', 'false')

        for provider, url in self.parse_conf['ProxyProviders'].items():
            clash_args = load_args('ClashProviders', provider)
            quanx_args = load_args('QuantumultXRemotes', provider)
            for x in ['clash', 'quanx']:
                subc_url = "http://{}/sub?url={}&{}".format(
                    self.subc, url, locals()[x+'_args'])
                print("{}'s {}: {}".format(provider, x, subc_url))
                txt = requests.get(subc_url).content.decode('utf-8', 'ignore')
                if self.check_if_available(txt, x, provider):
                    os.makedirs(f'{dir}/{x}/', exist_ok=True)
                    with open(f'{dir}/{x}/' + provider, 'w+') as f:
                        f.write(txt)

    def subconverter(self, read_dir, out_dir):
        if 'Subconverter' in self.parse_conf and type(self.parse_conf['Subconverter']) == list:
            _list = [ line for file in os.listdir(read_dir) for line in open(read_dir + '/' + file, 'r').readlines()]
            os.makedirs(out_dir, exist_ok=True)
            with open(out_dir + "/tmp_predefined", 'w') as f:
                f.writelines(_list)
            abs_path = os.path.abspath(out_dir + "/tmp_predefined")
            for target in self.parse_conf['Subconverter']:
                subc_url = "http://{}/sub?target={}&url={}".format(
                    self.subc, target, abs_path)
                subc_txt = requests.get(
                    subc_url).content.decode('utf-8', 'ignore')
                os.makedirs(out_dir, exist_ok=True)
                with open(out_dir+'/'+f"{target}.conf", 'w') as f:
                    txt = subc_txt.replace(self.subc, self.subc_remote)
                    f.write(txt)
            os.remove(out_dir + "/tmp_predefined")

    def classifier(self, read_dir):
        if 'Group Classify' in self.parse_conf:
            for provider, syntax in self.parse_conf['Group Classify'].items():
                if provider in self.unavailable_providers:
                    continue
                regExpresser.run(syntax, "{}/{}".format(read_dir, provider))
        else:
            print('Group Classify Disabled.')
