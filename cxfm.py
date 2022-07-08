#!/usr/bin/env python

import os
import subprocess
import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution

from loguru import logger
from chris_plugin import chris_plugin, PathMapper
from civet.obj import Surface
from civet.minc import MincVolume
from civet.xfm import TransformableMixin, Transformations, Xfm
from civet.memoization import Session
from concurrent.futures import ThreadPoolExecutor

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


DISPLAY_TITLE = r"""
       _              __           
      | |            / _|          
 _ __ | |________  _| |_ _ __ ___  
| '_ \| |______\ \/ /  _| '_ ` _ \ 
| |_) | |       >  <| | | | | | | |
| .__/|_|      /_/\_\_| |_| |_| |_|
| |                                
|_|                                
"""


parser = ArgumentParser(description='Perform XFM transformations on surfaces and masks',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--inputs', default='.mnc,.obj',
                    help='file extension of input files, comma-separated')
parser.add_argument('-s', '--scale', type=float, required=True,
                    help='Scale factor')
parser.add_argument('-r', '--rename', type=str, required=False,
                    help='String to insert before file extension of output files. '
                         "Use '%%s' to represent the value given for --scale")
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')


# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='MNI Xfm Transformations',
    category='Utility',
    min_memory_limit='200Mi',
    min_cpu_limit='1000m',
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    globs = ['**/*' + s for s in options.inputs.split(',')]
    mapper = PathMapper.file_mapper(inputdir, outputdir, glob=globs)
    scale = Xfm(Transformations.SCALES, options.scale, options.scale, options.scale)

    print(DISPLAY_TITLE, file=sys.stderr, flush=True)
    logger.info('Scale: {}', options.scale)
    logger.info('Input globs: {}', globs)

    with Session() as s:
        with ThreadPoolExecutor(max_workers=len(os.sched_getaffinity(0))) as pool:
            def process(input_file: Path, output_file: Path) -> None:
                if options.rename:
                    pre = options.rename.replace('%s', str(options.scale))
                    output_file = output_file.with_suffix(f'.{pre}{output_file.suffix}')
                try:
                    r = transformable(input_file).append_xfm(scale)
                    s.save(r, output_file)
                    logger.info('{} -> {}', input_file, output_file)
                except subprocess.CalledProcessError as e:
                    logger.exception(e)
                    # "fail-fast": cancel pending jobs on first failure
                    pool.shutdown(cancel_futures=True)
                    sys.exit(1)
            results = pool.map(lambda t: process(*t), mapper)

    # raise any uncaught exceptions
    for _ in results:
        pass


def transformable(p: Path) -> TransformableMixin:
    if p.suffix == '.obj':
        return Surface(p)
    if p.suffix == '.mnc':
        return MincVolume(p)
    logger.error('Unsupported file type for {}', p)
    raise ValueError(f'Unsupported file type: {p.suffix}')


if __name__ == '__main__':
    main()
