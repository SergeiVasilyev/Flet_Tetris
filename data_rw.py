import json


def save_data(filename, data):
    json_obj = json.dumps(data, indent=4)
    try:
        with open(filename, 'w') as f:
            f.write(json_obj)
        return True
    except:
        return None
    
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            obj = json.load(f)
        return obj
    except:
        return None
    
    

