#!/usr/bin/env python

import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution
from typing import Iterable

from loguru import logger
from chris_plugin import chris_plugin, PathMapper
from civet.obj import Surface
from civet.xfm import TransformableMixin, Transformations, Xfm
from civet.memoization import Session

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


parser = ArgumentParser(description='Perform XFM transformations on surfaces',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--inputs', default='.obj',
                    help='file extension of input files, comma-separated '
                         '(currently, only .obj is supported)')
parser.add_argument('-s', '--scale', type=float, required=True,
                    help='Scale factor')
parser.add_argument('-V', '--version', action='version',
                    version=f'$(prog)s {__version__}')


# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='MNI Xfm Transformations',
    category='Utility',
    min_memory_limit='200Mi',
    min_cpu_limit='1000m',
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, file=sys.stderr, flush=True)
    logger.info('Scale: {}', options.scale)
    mapper = multi_mapper(inputdir, outputdir, options.inputs)

    scale = Xfm(Transformations.SCALES, options.scale, options.scale, options.scale)

    with Session() as s:
        for input_file, output_file in mapper:
            r = transformable(input_file).append_xfm(scale)
            s.save(r, output_file)
            logger.info('{} -> {}', input_file, output_file)


def transformable(p: Path) -> TransformableMixin:
    if p.suffix == '.obj':
        return Surface(p)
    logger.error('Unsupported file type for {}', p)
    raise ValueError(f'Unsupported file type: {p.suffix}')


def multi_mapper(inputdir: Path, outputdir: Path, file_extensions: str) -> Iterable[tuple[Path, Path]]:
    for file_extension in file_extensions.split(','):
        yield from PathMapper(
            inputdir, outputdir,
            glob=f'**/*{file_extension}',
            suffix=file_extension,
            fail_if_empty=False
        )


if __name__ == '__main__':
    main()