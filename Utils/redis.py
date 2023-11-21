import json
import uuid
import decimal
from json import JSONEncoder
from datetime import datetime

class CustomSerializer(JSONEncoder):
    def default(self, value: any) -> str:
        if isinstance(value, uuid.UUID) or isinstance(value, datetime) or isinstance(value, decimal.Decimal) or isinstance(value, float):
            return str(value)
        return super(CustomSerializer, self).default(value)

def collapse_dictionary_for_hset(expanded_dict, flattened_dict, key):
    for k, v in expanded_dict.items():
        if key == '':
            next_key = k
        else:
            next_key = f'{key}:{k}'
        if isinstance(v, dict):
            collapse_dictionary_for_hset(v, flattened_dict, next_key)
        else:
            flattened_dict[next_key] = json.dumps(v, cls=CustomSerializer)
        
    return flattened_dict

def build_complex_dictionary(expanded_dict, k_split, v):
    if len(k_split) == 1:
        expanded_dict[k_split[0]] = json.loads(v)

    else:
        complex_key = k_split.pop(0)
        if complex_key not in expanded_dict:
            expanded_dict[complex_key] = dict()
        build_complex_dictionary(expanded_dict[complex_key], k_split, v)

def expand_dictionary_from_hget(collapsed_dict, expanded_dict):
    for k, v in collapsed_dict.items():
        if ':' not in k.decode():
            expanded_dict[k.decode()] = json.loads(v)
        else:
            k_split = k.decode().split(':')
            build_complex_dictionary(expanded_dict, k_split, v)

    return expanded_dict
