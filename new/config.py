import json
import os
import typing

cache = None

def setValue(key: str, value: str) -> None:
    config = getConfig()
    config[key] = value
    setConfig(config)

def getValue(key: str) -> typing.Any:
    config = getConfig()
    if key in config:
        return config[key]
    else:
        return None


def getConfig() -> dict:
    global cache
    if cache != None:
        return cache

    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            read = f.read()
            if not read:
                cache = {}
                return {}
            conf = json.loads(read)
            cache = conf
            return conf
    else:
        cache = {}
        return {}

def setConfig(config: dict) -> None:
    global cache
    cache = config
    with open('config.json', 'w') as f:
        f.write(json.dumps(config))