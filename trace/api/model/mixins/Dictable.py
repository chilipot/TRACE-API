from sqlalchemy.orm.collections import InstrumentedList


class Dictable(object):
    def as_dict(self, include_pk=True):
        fks = [fk.parent.name for fk in self.__table__.foreign_keys]
        pk = self.__table__.primary_key.columns.values()[0].name

        excluded_keys = fks
        if not include_pk:
            excluded_keys.append(pk)

        fields = {c.name: getattr(self, c.name) for c in self.__table__.columns
                  if c.name not in excluded_keys}

        for relationship in self.__mapper__.relationships:
            rel = relationship.key
            if rel not in getattr(self, 'exclude_dict_fields', []):
                rel_map = getattr(self, rel)
                if isinstance(rel_map, InstrumentedList):
                    # YO: Figure out better way to remove ID's from the "right" places
                    fields[rel] = [el.as_dict(include_pk=False) for el in rel_map]
                elif rel.startswith('lookup_'):
                    fields[rel.replace('lookup_', '')] = rel_map.as_dict().pop('text')
                else:
                    fields[rel] = rel_map.as_dict()

        return fields
