from django import template
import ast

register = template.Library()

@register.filter
def strToDict(value):
    list1 = []
    dict = ast.literal_eval(value)
    for key, value in dict.items():
        # print(key, value)
        str1 = value['color'] + ' - ' + value['length'] + ' - ' + value['width'] + ' - ' + str(value['quantity'])
        list1.append(str1)
    # print(list1)
    return list1
