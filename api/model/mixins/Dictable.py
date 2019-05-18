from sqlalchemy.orm.collections import InstrumentedList


class Dictable(object):
    # Fields to not include when as_dict() is called on Model type
    exclude_dict_fields = []
    # Whether to collapse dict to first property other than pk (to be used with simple objects with 1 other field)
    dict_collapse = False
    # Override to include pk when as_dict() is called (only considered when being nested)
    dict_carry_pk = True

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
            if rel not in self.exclude_dict_fields:
                rel_map = getattr(self, rel)
                if isinstance(rel_map, InstrumentedList):
                    fields[rel] = [self._dict_or_collapsed(el) for el in rel_map]
                else:
                    rel_fixed_name = rel.replace('lookup_', '') if rel.startswith('lookup_') else rel
                    fields[rel_fixed_name] = self._dict_or_collapsed(rel_map)

        return fields

    @staticmethod
    def _dict_or_collapsed(obj):
        if obj.dict_collapse:
            return obj.as_dict(include_pk=False).popitem()[1]
        else:
            return obj.as_dict(include_pk=obj.dict_carry_pk)
