import json
import logging
from pathlib import Path
from typing import Optional, Set, List, Union

import aiofiles

from ..models import PropertiesData, RentalProperty, SearchParams

logger = logging.getLogger(__name__)


class JSONStorage:
    
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        self._data: Optional[PropertiesData] = None
    
    async def load(self) -> PropertiesData:
        if not self.file_path.exists():
            logger.info(f"Storage file not found: {self.file_path}")
            
            self._data = PropertiesData(
                properties=[],
                search_params=SearchParams(),
            )
            return self._data
        
        try:
            async with aiofiles.open(self.file_path, "r", encoding="utf-8") as file:
                content = await file.read()
                data = json.loads(content)
                self._data = PropertiesData.from_dict(data)
                logger.info(
                    f"Loaded {self._data.total_properties} properties from {self.file_path}"
                )
                return self._data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            self._data = PropertiesData(
                properties=[],
                search_params=SearchParams(),
            )
            return self._data
        
        except Exception as e:
            logger.error(f"Failed to load storage: {e}")
            raise
    
    async def save(self, data: Optional[PropertiesData] = None):
        if data is not None:
            self._data = data
        
        if self._data is None:
            logger.error("No data to save")
            return
        
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            json_data = json.dumps(
                obj=self._data.to_dict(),
                ensure_ascii=False,
                indent=2,
            )
            
            async with aiofiles.open(self.file_path, "w", encoding="utf-8") as file:
                await file.write(json_data)
            
            logger.info(
                f"Saved {self._data.total_properties} properties to {self.file_path}"
            )

        except Exception as e:
            logger.error(f"Failed to save storage: {e}")
            raise
    
    async def add_properties(
        self,
        properties: List[RentalProperty],
        save: bool = True,
    ) -> List[RentalProperty]:
        if self._data is None:
            await self.load()
        
        new_properties = self._data.add_properties(properties)
        
        if save and new_properties:
            await self.save()
        
        return new_properties
    
    @property
    def data(self) -> Optional[PropertiesData]:
        return self._data
    
    @property
    def listing_ids(self) -> Set[str]:
        if self._data is None:
            return set()
        
        return self._data.listing_ids
    
    async def get_properties(
        self,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        rooms: Optional[List[int]] = None,
        limit: Optional[int] = None,
    ) -> List[RentalProperty]:
        
        if self._data is None:
            await self.load()
        
        properties = list(filter(
            lambda l: (min_price is None or l.price >= min_price) and 
                (max_price is None or l.price <= max_price) and
                (rooms is None or l.rooms in rooms),
            self._data.properties,
        ))

        properties = sorted(
            properties,
            key=lambda l: l.scraped_at,
            reverse=True,
        )
        
        if limit is not None:
            properties = properties[:limit]
        
        return properties
    
    async def update_search_params(self, params: SearchParams):
        if self._data is None:
            await self.load()
        
        self._data.search_params = params
        await self.save()
