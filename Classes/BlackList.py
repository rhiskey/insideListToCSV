from collections import namedtuple


def black_list_dict(dct):
    if 'nameOrg' in dct:
        return complex(dct['id'], dct['DT'], dct['nameOrg'])
    return dct


def blacklist_json_decode(blacklist_dict):
    return namedtuple('X', blacklist_dict.keys())(*blacklist_dict.values())


class BlackList:
    def __init__(self, id, DT, nameOrg):
        self.id = id
        self.DT = DT
        self.nameOrg = nameOrg