from django import template

register = template.Library()

@register.filter
def sort_by_name(users):
    return sorted(users, key=lambda u: (u.first_name, u.last_name))

@register.filter
def get_item(dictionary, key):
    """Custom filter to get an item from a dictionary by key."""
    if dictionary:
        return dictionary.get(key, None)
    return None

@register.filter
def get_item_0(dictionary, key):
    """Custom filter to access dictionary items by key."""
    return dictionary.get(key, 0)  # Returns 0 if the key doesn't exist