#!/usr/bin/env python

import json
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution

from chris_plugin import chris_plugin

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


DISPLAY_TITLE = r"""
ChRIS Plugin Template Title
"""


parser = ArgumentParser(description='cli description',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-n', '--name', default='foo',
                    help='argument which sets example output file name')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')

try :
    with open('flags.json') as fd:
        flags = json.load(fd)

    for f,v in flags.items():
        helpmsg = v['help'].replace("%", "")
        flag = "--"+f
        if v['type'] == 'bool':
            parser.add_argument(flag, help=helpmsg, dest=f, default=v['default'], action=v['action'])
        else:
            parser.add_argument(flag, help=helpmsg, dest=f, default=v['default'])
except FileNotFoundError:
    pass

# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='My ChRIS plugin',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='100Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE)

    output_file = outputdir / f'{options.name}.txt'
    output_file.write_text('did nothing successfully!')


if __name__ == '__main__':
    main()
