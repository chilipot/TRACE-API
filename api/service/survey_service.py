from sqlalchemy.orm import noload

from api.model import QuestionCategory, LookupQuestion
from api.utils.helpers import sort_and_paginate


def get_all_questions(page, page_size, order_by, category_ids=[]):
    return [q.as_dict() for q in sort_and_paginate(LookupQuestion.query, order_by, page, page_size).all()]
