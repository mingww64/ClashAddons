import os
import requests
import yaml
from . import classify


class pro:
    '''use class to handle variables change, 
otherwise vars will init before giving new config_path, 
which cause undefined / no such file errors'''  # i can use function though...
    config_path = './config.yaml'

    def __init__(self, path):
        if path != self.config_path:
            print("{} -> {}".format(self.config_path, path))
            self.__dict__['config_path'] = path

        config = open(self.config_path, 'r').read()
        parse_conf = yaml.safe_load(config)
        if not parse_conf['Enabled']:
            exit('Disabled.')
        self.subc = parse_conf['SCServer']
        self.subc_remote = parse_conf['SCServerRemote']
        self.head = parse_conf['Rules']['Clash']['head']
        self.rules = parse_conf['Rules']['Clash']['rules']
        self.parse_conf = parse_conf

    def check_if_available(self, content):
        if "The following link doesn't contain any valid node info:" in content or "No nodes were found!" in content:
            return False
        else:
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
                txt = requests.get(subc_url).content.decode('utf-8')
                if self.check_if_available(txt):
                    os.makedirs(f'{dir}/{x}/', exist_ok=True)
                    with open(f'{dir}/{x}/' + provider, 'w+') as f:
                        f.write(txt)

    def gen_quanx(self, exec_dir, out_dir):
        _list = []
        for file in os.listdir(exec_dir):
            with open(exec_dir + '/' + file, 'r') as f:
                _list += f.readlines()
        with open(out_dir + "/tmp_quanx", 'w') as f:
            f.writelines(_list)
        abs_path = os.path.abspath(out_dir + "/tmp_quanx")
        subc_url = "http://{}/sub?target=quanx&url={}".format(
            self.subc, abs_path)
        subc_txt = requests.get(subc_url).content.decode('utf-8')
        os.remove(out_dir + "/tmp_quanx")  # remove tmp after instantiation
        os.makedirs(out_dir, exist_ok=True)
        with open(out_dir+'/'+"quanx.conf", 'w') as f:
            txt = subc_txt.replace(self.subc, self.subc_remote)
            f.write(txt)

    def smart_filter(self, exec_dir):
        if 'SmartFilter' in self.parse_conf:
            for provider, syntax in self.parse_conf['SmartFilter'].items():
                classify.run(syntax, "{}/{}".format(exec_dir, provider))
        else: print('SmartFilter Disabled.')