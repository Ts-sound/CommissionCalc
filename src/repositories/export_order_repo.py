import os
import json
from typing import List

class ExportOrderRepository:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)
    
    def save(self, names: List[str]):
        order_file = os.path.join(self.config_dir, "export_order.json")
        data = {"names": names}
        with open(order_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self) -> List[str]:
        order_file = os.path.join(self.config_dir, "export_order.json")
        if not os.path.exists(order_file):
            return []
        with open(order_file, encoding='utf-8') as f:
            data = json.load(f)
        return data.get("names", [])