import pandas as pd
from typing import Dict, List

class ExcelRepository:
    def import_performance_data(self, file_path: str) -> Dict[str, float]:
        df = pd.read_excel(file_path)
        
        if "姓名" not in df.columns:
            raise ValueError("缺少'姓名'列")
        
        if "业绩" not in df.columns:
            raise ValueError("缺少'业绩'列")
        
        data = {}
        for _, row in df.iterrows():
            name = str(row["姓名"])
            performance = float(row["业绩"])
            data[name] = performance
        
        return data
    
    def export_results(self, results: List[Dict], file_path: str):
        df = pd.DataFrame(results)
        df.to_excel(file_path, index=False)