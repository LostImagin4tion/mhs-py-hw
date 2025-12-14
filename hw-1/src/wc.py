import sys
from typing import Tuple

import click


def count_stats(content_bytes: bytes) -> Tuple[int, int, int]:
    text: str = content_bytes.decode('utf-8', errors='replace')
    lines: int = text.count('\n')
    words: int = len(text.split())
    byte_count: int = len(content_bytes)
    return lines, words, byte_count


@click.command()
@click.argument('files', type=click.Path(exists=True), nargs=-1)
def wc(files: Tuple[str, ...]) -> None:
    if not files:
        content: bytes = sys.stdin.buffer.read()
        lines, words, bytes_count = count_stats(content)

        click.echo(f"{lines:8d}{words:8d}{bytes_count:8d}")
    else:
        total_lines: int = 0
        total_words: int = 0
        total_bytes: int = 0

        for filepath in files:
            with open(filepath, 'rb') as f:
                content = f.read()

            lines, words, bytes_count = count_stats(content)
            click.echo(f"{lines:8d}{words:8d}{bytes_count:8d} {filepath}")

            total_lines += lines
            total_words += words
            total_bytes += bytes_count
        
        if len(files) > 1:
            click.echo(f"{total_lines:8d}{total_words:8d}{total_bytes:8d} total")


if __name__ == '__main__':
    wc()
