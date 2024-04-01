from django import template

register = template.Library()

bad_list = ['накидаю', 'троеточия', 'символов', 'новость', 'статья']


@register.filter()
def censor(value):
    for word in bad_list:
        value = value.replace(word[1:], '*' * len(word[1:]))
    return value
