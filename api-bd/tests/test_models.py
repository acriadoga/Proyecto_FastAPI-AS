import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_item_tablename():
    from models import Item
    assert Item.__tablename__ == "items"


def test_item_columns():
    from models import Item
    cols = {c.name for c in Item.__table__.columns}
    assert cols == {"id", "nombre", "precio", "categoria_id"}


def test_item_id_is_primary_key():
    from models import Item
    assert Item.__table__.c.id.primary_key


def test_item_tiene_fk_a_categoria():
    from models import Item
    fk_targets = {fk.column.table.name for fk in Item.__table__.foreign_keys}
    assert "categorias" in fk_targets


def test_categoria_tablename():
    from models import Categoria
    assert Categoria.__tablename__ == "categorias"


def test_categoria_columns():
    from models import Categoria
    cols = {c.name for c in Categoria.__table__.columns}
    assert cols == {"id", "nombre"}


def test_tag_tablename():
    from models import Tag
    assert Tag.__tablename__ == "tags"


def test_tag_columns():
    from models import Tag
    cols = {c.name for c in Tag.__table__.columns}
    assert cols == {"id", "nombre"}


def test_tabla_intermedia_item_tag():
    from models import item_tag_association
    cols = {c.name for c in item_tag_association.columns}
    assert cols == {"item_id", "tag_id"}
