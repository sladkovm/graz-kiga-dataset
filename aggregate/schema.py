import json
from jsonschema import validate


schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "district": {"type": "string"},
            "name": {"type": "string"},
            "address": {"type": "string"},
            "tel": {"type": "string"},
            "n_groups": {"type": "string"},
            "time": {"type": "string"},
            "more": {"type": "string"},
            "GT": {"type": "number"},
            "lat": {"type": "number"},
            "lon": {"type": "number"},
            "location": {"type": ["object", "null"]},
        },
    }
}

if __name__ == "__main__":

    with open('data/krippe_privat.json') as f:
        kp = json.load(f)
        validate(kp, schema)

    with open('data/krippe_stad.json') as f:
        ks = json.load(f)
        validate(ks, schema)

    with open('data/kiga_privat.json') as f:
        kp = json.load(f)
        validate(kp, schema)

    with open('data/kiga_stad.json') as f:
        ks = json.load(f)
        validate(ks, schema)

    with open('data/landmarks.json') as f:
        ks = json.load(f)
        validate(ks, schema)