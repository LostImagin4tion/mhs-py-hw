import sys
from collections import deque
from typing import Tuple

import click


@click.command()
@click.argument('files', type=click.Path(exists=True), nargs=-1)
def tail(files: Tuple[str, ...]) -> None:
    if not files:
        lines: deque[str] = deque(sys.stdin, maxlen=17)
        for line in lines:
            click.echo(line, nl=False)
    else:
        is_multiple_files: bool = len(files) > 1

        for i, filepath in enumerate(files):
            if is_multiple_files:
                if i > 0:
                    click.echo()
                click.echo(f"==> {filepath} <==")
            
            with open(filepath, 'r') as f:
                lines = deque(f, maxlen=10)
                for line in lines:
                    click.echo(line, nl=False)


if __name__ == '__main__':
    tail()
 