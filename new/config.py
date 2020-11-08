import json
import os
import typing
import base64

cache = None

def encryptValue(key: str, value: str) -> None:
    setValue(key, base64.b85encode(value.encode()).decode())

def decryptValue(key: str) -> str:
    val = getValue(key)
    return base64.b85decode(val.encode()).decode()

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