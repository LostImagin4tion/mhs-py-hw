import asyncio
from pathlib import Path
from typing import List, Optional

import aiofiles
import aiohttp
import click


async def download_image(
    session: aiohttp.ClientSession,
    image_id: int,
    output_dir: Path,
    semaphore: asyncio.Semaphore,
) -> Optional[str]:
    width = 42
    height = 42
    url = f"https://picsum.photos/{width}/{height}"
    output_path = output_dir / f"image_{image_id:04d}.jpg"

    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()

                    async with aiofiles.open(output_path, "wb") as f:
                        await f.write(content)
                    
                    click.echo(f"Downloaded image successfully: {output_path}")
                    return str(output_path)
                else:
                    click.echo(
                        f"Failed to download image {image_id}",
                        err=True,
                    )
                    return None
        except aiohttp.ClientError as e:
            click.echo(f"Error while downloading image {image_id}: {e}", err=True)
            return None


async def download_images(
    count: int,
    output_dir: str,
) -> List[str]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    semaphore = asyncio.Semaphore(5)

    async with aiohttp.ClientSession() as session:
        tasks = [
            download_image(session, i, output_path, semaphore)
            for i in range(count)
        ]
        results = await asyncio.gather(*tasks)

    downloaded = [path for path in results if path is not None]

    click.echo(f"Successfully downloaded {len(downloaded)}/{count} images to {output_dir}")

    return downloaded


@click.command()
@click.option(
    "-n",
    "--count",
    type=int,
    default=5,
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default="hw-5/artifacts/task_5_1",
)
def main(count: int, output: str) -> None:
    asyncio.run(
        download_images(
            count=count,
            output_dir=output,
        )
    )


if __name__ == "__main__":
    main()
