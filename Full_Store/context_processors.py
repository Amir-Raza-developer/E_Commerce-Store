from products.models import Category


def global_context(request):
    """Make categories available in all templates for the navbar dropdown."""
    try:
        categories = Category.objects.all()
    except Exception:
        categories = []
    return {'categories': categories}
