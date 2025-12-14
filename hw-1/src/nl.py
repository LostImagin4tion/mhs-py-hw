from typing import TextIO

import click


@click.command()
@click.argument('file', type=click.File('r'), default='-', required=False)
def nl(file: TextIO) -> None:
    for line_num, line in enumerate(file, start=1):
        line_content: str = line.rstrip('\n')
        click.echo(f"{line_num:6d}\t{line_content}")


if __name__ == '__main__':
    nl()