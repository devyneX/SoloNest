from django import template

register = template.Library()


@register.filter(name="add_input_class")
def add_input_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name="add_label_class")
def add_label_class(field, css):
    return field.label_tag(attrs={"class": css})


# @register.filter
# def add_error_class(field, css):
#     pass
# return field.as_widget(attrs={"class": css})
