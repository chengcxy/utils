
import os
import json
from collections import OrderedDict


def get_title(db_type):
    mysql = OrderedDict({
        "host": "hosts",
        "port": "端口",
        "user": "用户名",
        "password": "密码",
        "db": "数据库",
        "charset": "编码"
    })
    influx = OrderedDict({
        "host": "hosts",
        "port": "端口",
        "username": "用户名",
        "password": "密码",
        "database": "数据库"
    })
    es = OrderedDict({
        "host": "hosts",
        "port": "端口",
        "http_auth": "http_auth"
    })

    mongo = OrderedDict({
        "host": "hosts",
        "port": "端口",
        "db": "数据库",
        "collection_name": "表"
    })
    item = eval(db_type)
    keys = [k for k in item.keys()]
    head = ["数据库类型"]
    head.extend([item[k] for k in keys])
    return keys, head


def get_markdown(vs):
    _keys = ['head', 'infos', 'db_type']
    head, infos, db_type = [vs[i] for i in _keys]
    str_head = '|' + '|'.join(head)
    t = [':-----' for i in head]
    head2 = '|' + '|'.join(t)
    ms = [str_head, head2]
    for value in infos:
        code = '|'.join(value)
        ms.append(code)
    return '\n'.join(ms)



def parse_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as fr:
        config = json.load(fr)
        return config


def get_storage(storage,config,key,split_flag):
    _from = config[key]
    db_types = [k for k in _from.keys()]
    for db_type in db_types:
        big_dict = _from[db_type]
        for k in big_dict.keys():
            db_info = big_dict[k]
            keys, head = get_title(db_type)
            _values = [db_type]
            _data = [str(db_info[k]) for k in keys]
            if db_type == 'mongo' and 'localhost' in _data:
                continue
            _values.extend(_data)
            storage.setdefault(db_type, set()).add(split_flag.join(_values))
    return storage


def write_md(markdown_file,_v):
    with open(markdown_file,'w',encoding='utf-8') as fw:
        data = '\n'.join([get_markdown(vs)+ '\n' for vs in _v])
        print(data)
        fw.write(data)



def main(config_file,markdown_file,split_flag):
    storage = {}
    config = parse_config(config_file)
    config_keys = [k for k in config.keys()]
    for key in config_keys:
        storage = get_storage(storage,config,key,split_flag)
    _v = []
    for db_type in storage.keys():
        keys, head = get_title(db_type)
        item = {'head': head, 'infos': [], 'db_type': db_type}
        for db_info in storage[db_type]:
            item['infos'].append(db_info.split(split_flag))
        _v.append(item)
    write_md(markdown_file,_v)
    return storage


if __name__ == '__main__':
    split_flag = '&'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(base_dir,'conf','db_config.json')
    markdown_file = os.path.join(base_dir, 'conf', 'db_info.md')
    storage = main(config_file,markdown_file,split_flag)
    print(markdown_file)
