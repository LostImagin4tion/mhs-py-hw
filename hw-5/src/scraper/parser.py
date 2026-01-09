import logging
import re
from typing import Optional, Pattern

from bs4 import BeautifulSoup, Tag

from ..models import RentalProperty

logger = logging.getLogger(__name__)


class CianParser:
    
    PRICE_PATTERN: Pattern[str] = re.compile(r"(\d[\d\s]*)")
    AREA_PATTERN: Pattern[str] = re.compile(r"(\d+(?:[.,]\d+)?)\s*м²?")
    FLOOR_PATTERN: Pattern[str] = re.compile(r"(\d+)/(\d+)")
    ROOMS_PATTERN: Pattern[str] = re.compile(r"(\d+)-комн|студия", re.IGNORECASE)
    ID_PATTERN: Pattern[str] = re.compile(r"/flat/(\d+)")
    
    def parse_listing_card(self, card_element: Tag) -> Optional[RentalProperty]:
        try:
            link_elem = card_element.select_one("a[href*='/rent/flat/']")

            if not link_elem:
                link_elem = card_element.select_one("a[href*='/flat/']")
            
            if not link_elem:
                logger.error("No link found in card")
                return None
            
            url = link_elem.get("href", "")

            if not url.startswith("http"):
                url = "https://cian.ru" + url
            
            url = url.split("?")[0]
            
            id_match = self.ID_PATTERN.search(url)

            if not id_match:
                logger.error(f"Could not extract ID from URL: {url}")
                return None
            
            listing_id = id_match.group(1)
            
            title = self._extract_title(card_element)
            price = self._extract_price(card_element)
            address = self._extract_address(card_element)
            rooms = self._extract_rooms(card_element, title)
            area = self._extract_area(card_element, title)
            floor = self._extract_floor(card_element, title)
            
            return RentalProperty(
                id=listing_id,
                title=title,
                price=price,
                address=address,
                rooms=rooms,
                area=area,
                floor=floor,
                url=url,
            )
            
        except Exception as e:
            logger.error(f"Error parsing listing card: {e}")
            return None
    
    def _extract_title(self, card: Tag) -> str:
        selectors = [
            "[data-name='LinkArea'] span",
            "[data-name='TitleComponent']",
            ".c6e8ba5398--title--",
            "a[href*='/rent/flat/']",
        ]
        
        for selector in selectors:
            elem = card.select_one(selector)

            if elem and elem.get_text(strip=True):
                return elem.get_text(strip=True)
        
        text = card.get_text(" ", strip=True)

        rooms_match = self.ROOMS_PATTERN.search(text)

        if rooms_match:
            start = max(0, rooms_match.start() - 5)
            end = min(len(text), rooms_match.end() + 30)
            return text[start:end].strip()
        
        return "Квартира"
    
    def _extract_price(self, card: Tag) -> int:
        selectors = [
            "[data-name='PriceComponent']",
            "[data-mark='PriceLabel']",
            ".c6e8ba5398--price--",
            "[class*='price']",
        ]
        
        for selector in selectors:
            elem = card.select_one(selector)

            if elem:
                text = elem.get_text(strip=True)

                match = self.PRICE_PATTERN.search(text)

                if match:
                    price_str = match.group(1).replace(" ", "").replace("\xa0", "")
                    try:
                        return int(price_str)
                    except ValueError:
                        continue
        
        return 0
    
    def _extract_address(self, card: Tag) -> str:
        selectors = [
            "[data-name='GeoLabel']",
            "[data-name='AddressComponent']",
            ".c6e8ba5398--address--",
            "[class*='address']",
            "[class*='geo']",
        ]
        
        for selector in selectors:
            elem = card.select_one(selector)

            if elem:
                text = elem.get_text(strip=True)
                if text and len(text) > 5:
                    return text
        
        return ""
    
    def _extract_rooms(self, card: Tag, title: str) -> int:
        if "студия" in title.lower():
            return 0  # Studio
        
        match = self.ROOMS_PATTERN.search(title)

        if match:
            rooms_str = match.group(1) if match.group(1) else "0"
            try:
                return int(rooms_str)
            except ValueError:
                pass
        
        text = card.get_text(" ", strip=True)
        if "студия" in text.lower():
            return 0
        
        match = self.ROOMS_PATTERN.search(text)

        if match:
            rooms_str = match.group(1) if match.group(1) else "0"
            try:
                return int(rooms_str)
            except ValueError:
                pass
        
        return 1  # Default to 1 room
    
    def _extract_area(self, card: Tag, title: str) -> float:
        match = self.AREA_PATTERN.search(title)

        if match:
            area_str = match.group(1).replace(",", ".")
            try:
                return float(area_str)
            except ValueError:
                pass
        
        selectors = [
            "[data-name='OfferSubtitle']",
            "[class*='area']",
            "[class*='subtitle']",
        ]
        
        for selector in selectors:
            elem = card.select_one(selector)

            if elem:
                text = elem.get_text(strip=True)
                match = self.AREA_PATTERN.search(text)
                
                if match:
                    area_str = match.group(1).replace(",", ".")
                    try:
                        return float(area_str)
                    except ValueError:
                        continue
        
        return 0.0
    
    def _extract_floor(self, card: Tag, title: str) -> str:
        match = self.FLOOR_PATTERN.search(title)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        
        selectors = [
            "[data-name='OfferSubtitle']",
            "[class*='floor']",
            "[class*='subtitle']",
        ]
        
        for selector in selectors:
            elem = card.select_one(selector)

            if elem:
                text = elem.get_text(strip=True)
                match = self.FLOOR_PATTERN.search(text)

                if match:
                    return f"{match.group(1)}/{match.group(2)}"
        
        return ""
    
    def parse_search_results(self, html: str) -> list[RentalProperty]:
        soup = BeautifulSoup(html, "lxml")
        properties = []
        
        card_selectors = [
            "[data-name='CardComponent']",
            "[data-testid='offer-card']",
            "article[data-name='CardComponent']",
            ".c6e8ba5398--card--",
            "[class*='--card--']",
        ]
        
        cards = []
        for selector in card_selectors:
            cards = soup.select(selector)
            if cards:
                logger.info(f"Found {len(cards)} cards with selector: {selector}")
                break
        
        if not cards:
            logger.error("No listing cards found, trying fallback method")
            links = soup.select("a[href*='/rent/flat/']")

            seen_hrefs = set()
            
            for link in links:
                href = link.get("href", "")

                if href and href not in seen_hrefs:
                    seen_hrefs.add(href)
                    parent = link.find_parent("article") or link.find_parent("div")

                    if parent:
                        cards.append(parent)
        
        for card in cards:
            listing = self.parse_listing_card(card)
            if listing:
                properties.append(listing)
        
        logger.info(f"Parsed {len(properties)} properties from page")
        return properties
    
    def get_total_pages(self, html: str) -> int:
        soup = BeautifulSoup(html, "lxml")
        
        pagination_selectors = [
            "[data-name='Pagination']",
            "[class*='pagination']",
            ".c6e8ba5398--pagination--",
        ]
        
        for selector in pagination_selectors:
            pagination = soup.select_one(selector)
            
            if pagination:
                page_links = pagination.select("a, span, li")
                max_page = 1
                
                for elem in page_links:
                    text = elem.get_text(strip=True)
                    if text.isdigit():
                        page_num = int(text)
                        max_page = max(max_page, page_num)
                
                if max_page > 1:
                    logger.info(f"Found {max_page} pages")
                    return max_page
        
        return 1
