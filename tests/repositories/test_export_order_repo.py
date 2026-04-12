import pytest
import os
import tempfile
from src.repositories.export_order_repo import ExportOrderRepository

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def export_order_repo(temp_dir):
    return ExportOrderRepository(temp_dir)

def test_save_export_order(export_order_repo):
    names = ["张三", "李四", "王五"]
    export_order_repo.save(names)
    
    order_file = os.path.join(export_order_repo.config_dir, "export_order.json")
    assert os.path.exists(order_file)

def test_load_export_order(export_order_repo):
    names = ["张三", "李四", "王五"]
    export_order_repo.save(names)
    
    loaded = export_order_repo.load()
    assert loaded == names

def test_load_empty_if_not_exists(export_order_repo):
    loaded = export_order_repo.load()
    assert loaded == []