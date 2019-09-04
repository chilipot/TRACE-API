from sqlalchemy.orm.collections import InstrumentedList


class Dictable(object):
    # Fields to not include when as_dict() is called on Model type
    exclude_dict_fields = []
    # Whether to collapse dict to first property other than pk (to be used with simple objects with 1 other field)
    dict_collapse = False
    # Override to include pk when as_dict() is called (only considered when being nested)
    dict_carry_pk = True

    def _as_dict_recur(self, models_hit, include_pk=True, override_exclude_dict_fields=[]):
        models_hit = models_hit + [self.__class__]

        fks = [fk.parent.name for fk in self.__table__.foreign_keys]
        pk = self.__table__.primary_key.columns.values()[0].name

        excluded_keys = fks
        if not include_pk:
            excluded_keys.append(pk)

        fields = {c.name: getattr(self, c.name) for c in self.__table__.columns
                  if c.name not in excluded_keys}

        exclude_dict_fields_list = override_exclude_dict_fields or self.exclude_dict_fields

        for relationship in self.__mapper__.relationships:
            rel = relationship.key
            if rel not in exclude_dict_fields_list and relationship.entity.class_ not in models_hit:
                rel_map = getattr(self, rel)
                if isinstance(rel_map, InstrumentedList):
                    fields[rel] = [self._dict_or_collapsed(el, models_hit) for el in rel_map]
                else:
                    rel_fixed_name = rel.replace('lookup_', '') if rel.startswith('lookup_') else rel
                    fields[rel_fixed_name] = self._dict_or_collapsed(rel_map, models_hit)

        return fields

    def as_dict(self, include_pk=True, override_exclude_dict_fields=[]):
        return self._as_dict_recur([self.__class__], include_pk, override_exclude_dict_fields)

    @staticmethod
    def _dict_or_collapsed(obj, models_hit=[]):
        if obj.dict_collapse:
            return next((v for k, v in obj._as_dict_recur(models_hit=models_hit, include_pk=False).items() if
                         k not in obj.exclude_dict_fields), None)
        else:
            return obj._as_dict_recur(models_hit=models_hit, include_pk=obj.dict_carry_pk)
