import re
import json

def loadModels():
    with open('data/models/models.json', 'r') as json_file:
        return json.load(json_file)

def searchModel(filename):
    match = re.search(r'_(\d+)_([^_]+)\.parquet', filename)
    models = loadModels()
    if match:
        return models[match.group(2)]
    return None

def getModelNames():
    models = loadModels()
    return [model['name'] for model in models.values()]