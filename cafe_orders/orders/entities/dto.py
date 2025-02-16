from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class OrderDTO:
    table_number: int
    items: List[Dict]
    status: str
    id: Optional[int] = field(default=None)
    total_price: Optional[float] = field(default=None)

@dataclass
class OrderUpdateDTO:
    items: list[Dict]
    status: str
    total_price: Optional[float] = field(default=None)



