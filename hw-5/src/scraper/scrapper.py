import logging
from typing import Optional, List, Tuple, Set
from urllib.parse import urlencode

from ..models import RentalProperty, SearchParams
from .client import AsyncHTTPClient
from .parser import CianParser

logger = logging.getLogger(__name__)


class CianScraper:
    
    BASE_URL = "https://www.cian.ru"
    
    CITY_IDS = {
        "moscow": 1,
        "spb": 2,
        "saint-petersburg": 2,
        "novosibirsk": 4897,
        "ekaterinburg": 4743,
        "kazan": 4777,
        "nizhny-novgorod": 4885,
        "samara": 4966,
        "rostov-on-don": 4959,
        "ufa": 5048,
    }
    
    def __init__(
        self,
        search_params: SearchParams,
        max_pages: int = 10,
    ):
        self.search_params = search_params
        self.max_pages = max_pages
        self.parser = CianParser()
        self._client: Optional[AsyncHTTPClient] = None
    
    def _build_search_url(self, page: int = 1) -> str:
        base_path = "/cat.php"
        params = {
            "deal_type": self.search_params.deal_type,
            "offer_type": "flat",
            "engine_version": "2",
        }
        
        city = self.search_params.city.lower()
        if city in self.CITY_IDS:
            params["region"] = self.CITY_IDS[city]
        elif city.isdigit():
            params["region"] = int(city)
        else:
            params["region"] = 1
            logger.error(f"Unknown city '{city}', defaulting to Moscow")
        
        if self.search_params.rooms:
            for room_count in self.search_params.rooms:
                if room_count == 0:
                    params["room0"] = 1  # Studio
                else:
                    params[f"room{room_count}"] = 1
        
        if self.search_params.min_price:
            params["minprice"] = self.search_params.min_price
        if self.search_params.max_price:
            params["maxprice"] = self.search_params.max_price
        
        if page > 1:
            params["p"] = page
        
        url = f"{self.BASE_URL}{base_path}?{urlencode(params)}"
        logger.info(f"Built search URL: {url}")
        return url
    
    async def scrape_page(
        self,
        client: AsyncHTTPClient,
        page: int = 1,
    ) -> Tuple[List[RentalProperty], int]:
        url = self._build_search_url(page)
        logger.info(f"Scraping page {page}: {url}")
        
        html = await client.get(url)
        if not html:
            logger.error(f"Failed to fetch page {page}")
            return [], 1
        
        properties = self.parser.parse_search_results(html)
        total_pages = self.parser.get_total_pages(html)
        
        logger.info(f"Found {len(properties)} properties on page {page}")
        return properties, total_pages
    
    async def scrape_all(self) -> List[RentalProperty]:
        all_properties: List[RentalProperty] = []
        seen_ids: Set[str] = set()
        
        async with AsyncHTTPClient() as client:
            properties, total_pages = await self.scrape_page(client, 1)
            
            for listing in properties:
                if listing.id not in seen_ids:
                    all_properties.append(listing)
                    seen_ids.add(listing.id)
            
            pages_to_scrape = min(total_pages, self.max_pages)
            logger.info(f"Total pages: {total_pages}, scraping up to {pages_to_scrape}")
            
            for page in range(2, pages_to_scrape + 1):
                properties, _ = await self.scrape_page(client, page)
                
                for listing in properties:
                    if listing.id not in seen_ids:
                        all_properties.append(listing)
                        seen_ids.add(listing.id)
                
                if not properties:
                    logger.info(f"No properties on page {page}, stopping")
                    break
        
        logger.info(f"Total unique properties scraped: {len(all_properties)}")
        return all_properties
    
    async def find_new_properties(
        self,
        existing_ids: set[str],
        max_pages: int = 3,
    ) -> List[RentalProperty]:
        new_properties = []
        
        async with AsyncHTTPClient() as client:
            for page in range(1, max_pages + 1):
                properties, _ = await self.scrape_page(client, page)
                
                page_new = [
                    listing for listing in properties
                    if listing.id not in existing_ids
                ]
                
                new_properties.extend(page_new)
                
                if not page_new and page > 1:
                    logger.info(f"No new properties on page {page}, stopping search")
                    break
        
        logger.info(f"Found {len(new_properties)} new properties")
        return new_properties
