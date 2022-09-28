#!/usr/bin/env python

import json
import os
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution
import subprocess
import sys

from chris_plugin import chris_plugin

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


DISPLAY_TITLE = r"""
ChRIS Plugin Template Title
"""


parser = ArgumentParser(description='cli description',
                        formatter_class=ArgumentDefaultsHelpFormatter)
# parser.add_argument('-n', '--name', default='foo',
#                     help='argument which sets example output file name')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')

parser.add_argument('--dry-run', action='store_true',
                    help='Do not run commands, instead print the commands to be issued')

#-------------------------------------------------------------------------------------------------
# Generic code for loading supported flags from 'flags.json' which is automatically generated 
# by parsing the output of '<commandname> --help'. See 'prepare_flags.py' for more information 
#-------------------------------------------------------------------------------------------------

try :
    with open('flags.json') as fd:
        flags = json.load(fd)

    for f,v in flags.items():
        helpmsg = v['help'].replace("%", "")
        flag = "--"+f  # TODO: Add code to handle single letter options, i.e., with single '-'
        if v['type'] == 'bool':
            parser.add_argument(flag, help=helpmsg, dest=f, default=v['default'], action=v['action'])
        else:
            parser.add_argument(flag, help=helpmsg, dest=f, default=v['default'])
except FileNotFoundError:
    flags = None
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

    # output_file = outputdir / f'{options.name}.txt'
    # output_file.write_text('did nothing successfully!')

    #-------------------------------------------------------------------------------------------------
    # Generic code for invoking standalone external programs (for DS type plugin).
    # It may need to be manually adapted for specific target program.
    #-------------------------------------------------------------------------------------------------

    cmd = os.path.join('/usr/bin', sys.argv[0].split('/')[-1])

    # TODO: replace code below with a more generic (not jpegoptim) method for handling outdir
    cmdline = [cmd, "--dest={}".format(options.outputdir)]

    # If 'flags.json' files exists in working directory, load it
    try:
        global flags
        if flags == None : 
            with open('flags.json') as fd:
                flags = json.load(fd)

    except FileNotFoundError as exp:
        pass


    # Add every non-default option to command line
    # TODO: add code to handle single letter flags, i.e., those with single '-'
    for k, v in options.__dict__.items():

        try:
            default = flags[k]['default']
            if v != default:
                if isinstance(v,bool) :
                    option = "--{}".format(k)
                else:
                    option = "--{}={}".format(k, v)
                cmdline.append(option)
        except:
            continue

    # for every file in options.inputdir invoke command line
    for  file in os.listdir(options.inputdir):
        file_fullpath = os.path.join(options.inputdir, file)
        if options.dry_run:
            print(cmdline + [file_fullpath])
        else:
            subprocess.run(cmdline + [file_fullpath], check=True)


if __name__ == '__main__':
    main()
