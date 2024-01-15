import yaml
path= "file.yml"
def parse(path):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    
    for endpoints in config:
        if endpoints.get('method') is None:
            print('GET')
        else:
            print(endpoints)


parse(path)