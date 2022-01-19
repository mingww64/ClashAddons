from string import Template
import os, requests, re
class Proxy:
  '''self represents the instance of the class.'''
  urltest="""
  url: http://www.gstatic.com/generate_204
  interval: '300'
  tolerance: '150'
  """
  rules = requests.get('https://raw.githubusercontent.com/lhie1/Rules/master/Clash/Rule.yaml').content.decode('utf-8')
  head = requests.get('https://raw.githubusercontent.com/lhie1/Rules/master/Clash/Head_dns.yaml').content.decode('utf-8')
  def __init__(self):
    self.proxy_providers = Template("""
\t${name}:
\t\ttype: http
\t\tpath: "./proxy_provider/${name}.yaml"
\t\turl: https://cdn.jsdelivr.net/gh/wmyfelix/ClashAddons@OMC/proxies/Clash/${name}
\t\tinterval: 3600
\t\thealth-check:
\t\t  enable: true
\t\t  url: http://www.gstatic.com/generate_204
\t\t  interval: 300
    """)
    self.proxy_group = Template("""
- name: ${name}
  type: ${type}
  ${proxies}
  ${uses}
  ${urltest}
    """)
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
        if x == 'AdBlock': ret += self.proxy_group.substitute(name = x, type = 'select', proxies = "proxies:\n" + '\t- REJECT\n\t- DIRECT\n\t- Proxy', uses = '', urltest = '')
        elif x == 'DIRECT': continue
        elif x == 'Proxy': ret += self.proxy_group.substitute(name = x, type = 'select', proxies = "proxies:\n\t- All\n" + all_proxies()+'\n\t- DIRECT', uses = '', urltest = '')
        else: ret += self.proxy_group.substitute(name = x, type = 'select', proxies = 'proxies:\n\t- Proxy\n'+all_proxies() + '\n\t- DIRECT', uses = '', urltest = '')
      return ret
    return self.proxy_group.substitute(name = 'All', type = 'url-test', proxies = "proxies:\n" + all_proxies(), uses = '', urltest = self.urltest) + gen_rules()
  def gen_each_proxies(self):
    ret = ""
    for x in self.list_name:
      ret += self.proxy_group.substitute(name = x, type = 'url-test', proxies = '', uses = f"use:\n\t- {x}", urltest = self.urltest)
    return ret
proxy = Proxy() # instance: proxy
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
  file = file.replace('\t','  ')
  with open('test.yaml','w') as f:
    f.write(file)    
arranger()