import json
import os
from pathlib import Path
from typing import Optional


class CatalogService:
    def __init__(self):
        """Initialize catalog service."""
        catalog_path = Path(__file__).parent.parent.parent / "catalog" / "catalog.json"
        self.catalog_path = catalog_path
        self.catalog = self._load_catalog()
    
    def _load_catalog(self) -> list:
        """Load catalog from JSON file."""
        try:
            with open(self.catalog_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading catalog: {str(e)}")
            return []
    
    def get_all_items(self) -> list:
        """Get all catalog items."""
        return self.catalog
    
    def get_item_by_id(self, jewelry_id: str) -> Optional[dict]:
        """Get catalog item by ID."""
        for item in self.catalog:
            if item.get('id') == jewelry_id:
                return item
        return None
    
    def get_items_by_type(self, jewelry_type: str) -> list:
        """Get all items of a specific type."""
        return [item for item in self.catalog if item.get('type') == jewelry_type]


# Singleton instance
_catalog_service = None


def get_catalog_service() -> CatalogService:
    """Get or create catalog service instance."""
    global _catalog_service
    if _catalog_service is None:
        _catalog_service = CatalogService()
    return _catalog_service
