import os
import json
def env(args):
    environment = __parseSpringApplicationJson()
    for arg in args:
        if (arg.startswith('--')):
            (key,value)=arg.split("=")
            key = key.replace('--','')
            environment[key]=value
    return environment

def __parseSpringApplicationJson():
    environment={}
    try:
        springApplicationJson=os.environ['SPRING_APPLICATION_JSON']
        if (springApplicationJson):
            environment=json.loads(springApplicationJson)
    except:
        pass
    return environment

