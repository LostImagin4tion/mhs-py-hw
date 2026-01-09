import asyncio
import logging
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List

import click

from src.models import SearchParams
from src.scraper import CianScraper
from src.data import JSONStorage


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


DEFAULT_STORAGE_PATH = Path("artifacts/task_5_2/properties.json")


def parse_rooms(ctx, param, value: Optional[str]) -> Optional[List[int]]:
    if value is None:
        return None
    
    try:
        rooms = [int(r.strip()) for r in value.split(",")]
        return rooms
    except ValueError:
        raise click.BadParameter("Rooms must be comma-separated integers (e.g., '1,2,3')")


@click.command()
@click.option(
    "--city",
    default="moscow",
    help="City to search in",
    show_default=True,
)
@click.option(
    "--rooms",
    callback=parse_rooms,
    help="Room counts, comma-separated",
)
@click.option(
    "--min-price",
    type=int,
    help="Minimum monthly rent",
)
@click.option(
    "--max-price",
    type=int,
    help="Maximum monthly rent",
)
@click.option(
    "--interval",
    type=int,
    default=30,
    help="Check interval in minutes",
    show_default=True,
)
@click.option(
    "--max-pages",
    type=int,
    default=3,
    help="Max pages to check for new properties",
    show_default=True,
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default=str(DEFAULT_STORAGE_PATH),
    help="Output JSON file path",
    show_default=True,
)
def main(
    city: str,
    rooms: Optional[list[int]],
    min_price: Optional[int],
    max_price: Optional[int],
    interval: int,
    max_pages: int,
    output: str,
) -> None:
    click.echo(f"Starting Cian scrapper for {city}...")
    click.echo(f"Interval: every {interval} minutes")
    
    search_params = SearchParams(
        city=city,
        deal_type="rent",
        rooms=rooms,
        min_price=min_price,
        max_price=max_price,
    )
    
    running = True
    
    def handle_signal(signum, frame):
        nonlocal running
        click.echo("\nShutting down...")
        running = False
    
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    async def do_monitor():
        storage = JSONStorage(output)
        await storage.load()
        await storage.update_search_params(search_params)
        
        scraper = CianScraper(
            search_params=search_params,
            max_pages=max_pages,
        )
        
        check_count = 0
        total_new = 0
        
        while running:
            check_count += 1
            timestamp = datetime.now().strftime("%Y-x%m-%d %H:%M:%S")
            click.echo(f"[{timestamp}] Check #{check_count}")
            
            try:
                new_properties = await scraper.find_new_properties(
                    existing_ids=storage.listing_ids,
                    max_pages=max_pages,
                )
                
                if new_properties:
                    added = await storage.add_properties(new_properties)
                    total_new += len(added)
                    
                    click.echo(f"\tFound {len(added)} new properties!")

                    for listing in added[:3]:
                        click.echo(
                            f"\t\t--> {listing.title} | {listing.price:,} рублей"
                        )
                        click.echo(f"\t\t{listing.url}")
                    
                    if len(added) > 3:
                        click.echo(f"\t... and {len(added) - 3} more")
                else:
                    click.echo("\tNo new properties found")
                
                click.echo(
                    f"\tTotal stored: {storage.data.total_properties} | "
                    f"New: {total_new}"
                )
                
            except Exception as e:
                logger.error(f"Error during check: {e}")
                click.echo(f"\tError: {e}", err=True)
            
            if running:
                click.echo(f"\tNext check in {interval} minutes...\n")

                for _ in range(interval * 60):
                    if not running:
                        break
                    
                    await asyncio.sleep(1)
        
        click.echo(f"Scrapper stopped. Total new properties found: {total_new}")
    
    asyncio.run(do_monitor())


if __name__ == "__main__":
    main()
