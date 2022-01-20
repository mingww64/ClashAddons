# WIP.
import yaml, requests, os
file = yaml.safe_load(open('config.yaml','r'))
providers = (file['ProxyProviders'])
for x in providers:
    y = providers[x]
    try:
        response = requests.get(y,allow_redirects=True).content.decode('utf-8')
        if not os.path.isdir('./testdir'):
            os.mkdir('./testdir')
        with open('testdir/'+x,'w') as f:
            f.write(response)
    except requests.exceptions.ConnectionError:
        print('err')
