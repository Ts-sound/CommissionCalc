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
        
        numeric_cols = ["业绩", "提成点数", "个人提成", "团队提成", "管理提成", "高业绩奖金", "销冠奖金", "总提成"]
        for col in numeric_cols:
            if col in df.columns:
                if col == "提成点数":
                    continue
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        df.to_excel(file_path, index=False, engine="openpyxl")