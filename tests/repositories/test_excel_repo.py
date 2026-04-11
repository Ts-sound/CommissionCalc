import pytest
import pandas as pd
import tempfile
import os
from src.repositories.excel_repo import ExcelRepository

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def excel_repo(temp_dir):
    return ExcelRepository()

@pytest.fixture
def sample_excel_file(temp_dir):
    df = pd.DataFrame({
        "姓名": ["张三", "李四", "王五"],
        "业绩": [5000, 3000, 15000]
    })
    file_path = os.path.join(temp_dir, "test.xlsx")
    df.to_excel(file_path, index=False)
    return file_path

def test_import_performance_data(excel_repo, sample_excel_file):
    data = excel_repo.import_performance_data(sample_excel_file)
    
    assert len(data) == 3
    assert data["张三"] == 5000.0
    assert data["李四"] == 3000.0
    assert data["王五"] == 15000.0

def test_import_missing_column(excel_repo, temp_dir):
    df = pd.DataFrame({"姓名": ["张三"]})
    file_path = os.path.join(temp_dir, "invalid.xlsx")
    df.to_excel(file_path, index=False)
    
    with pytest.raises(ValueError, match="缺少'业绩'列"):
        excel_repo.import_performance_data(file_path)

def test_export_results(excel_repo, temp_dir):
    results = [
        {
            "姓名": "张三",
            "业绩": 5000,
            "身份": "组长",
            "组别": "A组",
            "个人提成": 1000,
            "团队提成": 800,
            "管理提成": 200,
            "高业绩奖金": 500,
            "总提成": 2500
        }
    ]
    
    export_path = os.path.join(temp_dir, "result.xlsx")
    excel_repo.export_results(results, export_path)
    
    assert os.path.exists(export_path)
    
    df = pd.read_excel(export_path)
    assert len(df) == 1
    assert df.iloc[0]["姓名"] == "张三"
    assert df.iloc[0]["总提成"] == 2500