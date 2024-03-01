import json


def save_score(name, score):
    obj = {
        'name': name,
        'score': score
    }
    json_obj = json.dumps(obj, indent=4)
    try:
        with open('highscore.json', 'w') as f:
            f.write(json_obj)
    except:
        return None


def read_score():
    try:
        with open('highscore.json', 'r') as f:
            obj = json.load(f)
    except:
        return None
    return obj


if __name__ == '__main__':
    
    print(read_score())