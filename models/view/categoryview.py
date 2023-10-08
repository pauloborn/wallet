from lazyutils.structure.Singleton import Singleton
from sqlalchemy.orm import Session

from models.BankStatements import Category, Subcategory


class CategorySubcategoryNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CategoryView(Singleton):
    category_map = None
    subcategory_map = None

    def __init__(self, session: Session):
        self.session = session

    def category_id_from_name(self, name: str) -> int:
        name = name.replace('\n', '').replace('\t', '')

        if self.category_map is None:
            self.category_map = {}
            for cat in self.session.query(Category).all():
                self.category_map[cat.name] = cat.id

        if name in self.category_map:
            return self.category_map[name]
        else:
            raise CategorySubcategoryNotFound

    def subcategory_id_from_name(self, name: str, category_id: int) -> int:
        name = name.replace('\n', '').replace('\t', '')

        if self.subcategory_map is None:
            self.subcategory_map = {}
            for scat in self.session.query(Subcategory).all():
                self.subcategory_map[f"{scat.category_id}-{scat.name}"] = scat.id

        subcategory_metaname = f"{category_id}-{name}"
        if subcategory_metaname in self.subcategory_map:
            return self.subcategory_map[subcategory_metaname]
        else:
            raise CategorySubcategoryNotFound
