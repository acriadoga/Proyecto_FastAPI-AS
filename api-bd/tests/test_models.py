import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_item_tablename():
    from models import Item
    assert Item.__tablename__ == "items"

def test_item_columns():
    from models import Item
    cols = {c.name for c in Item.__table__.columns}
    assert cols == {"id", "nombre", "descripcion", "precio", "en_stock"}

def test_item_id_is_primary_key():
    from models import Item
    assert Item.__table__.c.id.primary_key

def test_item_en_stock_default_true():
    from models import Item
    assert Item.__table__.c.en_stock.default.arg is True
