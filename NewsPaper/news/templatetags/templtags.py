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
