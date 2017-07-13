from konlpy.tag import Mecab
from skku.models import Category, Keyword
from django.core.cache import cache


def extract_category(user_key, content):
    categorys = set(c.name for c in Category.objects.all())
    mecab = Mecab()
    nouns_set = set(mecab.nouns(content))
    category_name = list(categorys & nouns_set)

    if len(category_name) != 1:
        return None
    category = Category.objects.get(name=category_name[0])
    cache.set(user_key, category)
    return category


def extract_keyword(category, content):
    keywords = set(k for k in Keyword.objects.values_list('name', flat=True))

    arguments = category.arguments
    required_type = set(a.type for a in arguments if not a.option)
    mecab = Mecab()
    nouns_set = set(mecab.nouns(content))
    keyword = keywords & nouns_set

    if len(required_type - keyword) != 0:
        return False, {
            "message": {
                "text": (required_type - keyword).pop().error
            }
        }

    return True, list(keyword)
