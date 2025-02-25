from django import template
from string import punctuation

register = template.Library()

bad_words = [
    'туфта', 'говно', 'имбецил', 'дебил',
    'наркотиками', 'наркотики'
]
@register.filter(name='censor')
def cut_bad_words(value: str):
    """
    value: Post[title, text] or Comment[text] object.
    Checking for incorrect words. Splitting the text to check for matches.
    """
    text = value.split(' ')
    result = []
    for t in text:
        if t.strip(punctuation).lower() in bad_words:
            t = t[0] + ('*' * (len(t) - 1))
        result.append(t)
    return ' '.join(result)

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()

@register.filter(name='splitter')
def cut_path(string: str, delete_part: str) -> str:
    string.strip(delete_part + '/')
    return string