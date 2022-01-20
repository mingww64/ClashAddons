from string import Template
import os, requests, re, yaml
from tempfile import template
class Proxy:
  '''self represents the instance of the class.'''
  rules = requests.get('https://raw.githubusercontent.com/lhie1/Rules/master/Clash/Rule.yaml').content.decode('utf-8')
  head = requests.get('https://raw.githubusercontent.com/lhie1/Rules/master/Clash/Head_dns.yaml').content.decode('utf-8')
  def __init__(self):
    names = self.__dict__
    for x in ['proxy_groups','proxy_providers','urltest']:
      template_file = './template/clash/'+x
      if os.path.isfile(template_file):
        y = open(template_file).read()
      else: print(f"template: {x} not exist.",exit())

      names[x] = Template(y)
    self.urltest = self.urltest.substitute(url = 'http://www.gstatic.com/generate_204', interval = 300, tolerance = 180)
    self.list_name = os.listdir('./proxies/Clash')
  def gen_proxy_providers(self):
    ret = ""
    for x in self.list_name:
      ret += self.proxy_providers.substitute(name = x)
    return ret
  def gen_all_proxies(self):
    def all_proxies():
      ret = ""
      for x in self.list_name:
          ret += f"\t- {x}\n"
      return ret
    def gen_rules():
      sets = re.findall('.*RULE-SET.*',self.rules)
      rules_proxies = ['Others']
      for x in sets:
        rule_name = re.split(',',x)[-1]
        if rule_name not in rules_proxies:
          rules_proxies.append(rule_name)
      ret = ""
      for x in rules_proxies:
        if x == 'AdBlock': ret += self.proxy_groups.substitute(name = x, type = 'select', proxies = "proxies:\n" + '\t- REJECT\n\t- DIRECT\n\t- Proxy', uses = '', urltest = '')
        elif x == 'DIRECT': continue
        elif x == 'Proxy': ret += self.proxy_groups.substitute(name = x, type = 'select', proxies = "proxies:\n\t- All\n" + all_proxies()+'\n\t- DIRECT', uses = '', urltest = '')
        elif x == 'Domestic': ret += self.proxy_groups.substitute(name = x, type = 'select', proxies = 'proxies:\n\t- DIRECT\n' + '\n\t- Proxy\n' + all_proxies(), uses = '', urltest = '')
        else: ret += self.proxy_groups.substitute(name = x, type = 'select', proxies = 'proxies:\n\t- Proxy\n'+all_proxies() + '\n\t- DIRECT', uses = '', urltest = '')
      return ret
    return self.proxy_groups.substitute(name = 'All', type = 'url-test', proxies = "proxies:\n" + all_proxies(), uses = '', urltest = self.urltest) + gen_rules()
  def gen_each_proxies(self):
    ret = ""
    for x in self.list_name:
      ret += self.proxy_groups.substitute(name = x, type = 'url-test', proxies = '', uses = f"use:\n\t- {x}", urltest = self.urltest)
    return ret
proxy = Proxy() # instance: proxy
def get_list(file):
  return yaml.dump(file)
def arranger():
  file = f"""
{proxy.head}
proxy-providers:
{proxy.gen_proxy_providers()}
proxy-groups:
{proxy.gen_all_proxies()}
{proxy.gen_each_proxies()}
rules:
{proxy.rules}
  """
  file = file.replace('\t','  ') # YAML dont support Tabulator key.
  with open('test.yaml','w') as f:
    f.write(file)    
arranger()