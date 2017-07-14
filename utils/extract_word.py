from konlpy.tag import Mecab
from skku.models import Category, Keyword, Argument
from django.core.cache import cache


def extract_category(user_key, content):
    categorys = set(c.name for c in Category.objects.all())
    mecab = Mecab()
    nouns_set = set(mecab.nouns(content))
    category_name = list(categorys & nouns_set)

    if len(category_name) != 1:
        return None
    category = Category.objects.get(name=category_name[0])
    category.count = category.count + 1
    category.save()
    cache.set(user_key, category)
    return category


def extract_keyword(category, content):
    keywords = Keyword.objects.all()
    keywords_name = set(k for k in keywords.values_list('name', flat=True))

    arguments = Argument.objects.filter(category=category)
    required_type = set(a.type for a in arguments if not a.option)
    mecab = Mecab()
    nouns_set = set(mecab.nouns(content))
    error = ['수강신청', '강의평가']
    for e in error:
        if e in content:
            nouns_set.add(e)
    keyword = keywords_name & nouns_set

    keyword_type = set(k for k in keywords.filter(name__in=keyword).values_list('type', flat=True))

    if len(required_type - keyword_type) != 0:
        return False, {
            "message": {
                "text": arguments.filter(type=(required_type - keyword_type).pop()).get().error
            }
        }

    return True, list(keyword)
