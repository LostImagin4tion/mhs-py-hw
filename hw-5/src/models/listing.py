from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

@dataclass
class SearchParams:
    
    city: str = "moscow"
    deal_type: str = "rent"
    rooms: Optional[list[int]] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "city": self.city,
            "deal_type": self.deal_type,
            "rooms": self.rooms,
            "min_price": self.min_price,
            "max_price": self.max_price,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchParams":
        return cls(
            city=data.get("city", "moscow"),
            deal_type=data.get("deal_type", "rent"),
            rooms=data.get("rooms"),
            min_price=data.get("min_price"),
            max_price=data.get("max_price"),
        )


@dataclass
class RentalProperty:
    
    id: str
    title: str
    price: int
    address: str
    rooms: int
    area: float
    floor: str
    url: str
    scraped_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "address": self.address,
            "rooms": self.rooms,
            "area": self.area,
            "floor": self.floor,
            "url": self.url,
            "scraped_at": self.scraped_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RentalProperty":
        scraped_at = data.get("scraped_at")

        if isinstance(scraped_at, str):
            scraped_at = datetime.fromisoformat(scraped_at)
        elif scraped_at is None:
            scraped_at = datetime.now(timezone.utc)
            
        return cls(
            id=data["id"],
            title=data["title"],
            price=data["price"],
            address=data["address"],
            rooms=data["rooms"],
            area=data["area"],
            floor=data["floor"],
            url=data["url"],
            scraped_at=scraped_at,
        )


@dataclass
class PropertiesData:
    
    properties: List[RentalProperty]
    search_params: SearchParams
    last_updated: datetime = field(default_factory=datetime.now)
    
    @property
    def total_properties(self) -> int:
        return len(self.properties)
    
    @property
    def listing_ids(self) -> set[str]:
        return {listing.id for listing in self.properties}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": {
                "last_updated": self.last_updated.isoformat(),
                "total_properties": self.total_properties,
                "search_params": self.search_params.to_dict(),
            },
            "properties": [listing.to_dict() for listing in self.properties],
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PropertiesData":
        metadata = data.get("metadata", {})
        last_updated = metadata.get("last_updated")

        if isinstance(last_updated, str):
            last_updated = datetime.fromisoformat(last_updated)
        elif last_updated is None:
            last_updated = datetime.now(timezone.utc)
            
        search_params = SearchParams.from_dict(
            metadata.get("search_params", {})
        )
        
        properties = [
            RentalProperty.from_dict(item)
            for item in data.get("properties", [])
        ]
        
        return cls(
            properties=properties,
            search_params=search_params,
            last_updated=last_updated,
        )
    
    def add_properties(self, new_properties: List[RentalProperty]) -> List[RentalProperty]:
        existing_ids = self.listing_ids
        actually_new: List[RentalProperty] = []
        
        for listing in new_properties:
            if listing.id not in existing_ids:
                self.properties.append(listing)
                actually_new.append(listing)
                
        self.last_updated = datetime.now(timezone.utc)

        return actually_new
