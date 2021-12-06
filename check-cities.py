from typing import Any

import jadn
import json
import os

DATA_DIR = 'World'


def load_any(path: str) -> (dict, None):
    fn, ext = os.path.splitext(path)
    try:
        loader = {
            '.jadn': jadn.load,
            '.jidl': jadn.convert.jidl_load,
            '.html': jadn.convert.html_load
        }[ext]
    except KeyError:
        if os.path.isfile(path):
            raise ValueError(f'Unsupported schema format: {path}')
        return
    return loader(path)


def process(file: (str, bytes), schema: dict, verbosity: str) -> Any:
    vr = {'v': True, 'c': False, 'z': False}[verbosity]
    vs = {'v': True, 'c': True, 'z': False}[verbosity]
    codec = jadn.codec.Codec(schema, verbose_rec=vr, verbose_str=vs)
    return codec.decode('World', json.load(file))


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}')
    os.chdir(DATA_DIR)
    for schema_file in [fn for f in os.listdir('.') if (fn := os.path.splitext(f))[1] == '.jidl']:
        sc = load_any(''.join(schema_file))
        print(f'\n{schema_file[0]}:\n', '\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(sc)).items()]))
        for v in ('v', 'c', 'z'):
            try:
                with open(schema_file[0] + v + '.json') as fp:
                    info = process(fp, sc, v)
                    print(f'  {fp.name}: {info}')
            except FileNotFoundError:
                pass
