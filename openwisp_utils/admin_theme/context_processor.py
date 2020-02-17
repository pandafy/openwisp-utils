from django.apps import registry
from django.conf import settings
from django.contrib.admin import site
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse


def menu_items(request):
    menu = build_menu(request)
    return {
        'openwisp_menu_items': menu,
        'show_userlinks_block': getattr(
            settings,
            'OPENWISP_ADMIN_SHOW_USERLINKS_BLOCK',
            False
        )
    }


def build_menu(request=None):
    default_items = getattr(settings, 'OPENWISP_DEFAULT_ADMIN_MENU_ITEMS', [])
    custom_items = getattr(settings, 'OPENWISP_ADMIN_MENU_ITEMS', [])
    items = custom_items or default_items
    menu = []
    # loop over each item to build the menu
    # and check user has permission to see each item
    for item in items:
        app_label, model = item['model'].split('.')
        model_class = registry.apps.get_model(app_label, model)
        url = reverse('admin:{}_{}_changelist'.format(app_label,
                                                      model.lower()))
        label = item.get('label', model_class._meta.verbose_name_plural)
        model_admin = site._registry[model_class]
        if not request or model_admin.has_module_permission(request):
            menu.append({
                'url': url,
                'label': label,
                'class': model.lower()
            })
    return menu


def customize_admin_theme(request):
    openwisp_admin_css = getattr(settings, 'OPENWISP_ADMIN_THEME_CSS', [])
    openwisp_admin_js = getattr(settings, 'OPENWISP_ADMIN_JS', [])
    is_list_of_str = all(isinstance(item, str) for item in openwisp_admin_css)
    if not isinstance(openwisp_admin_css, list) or not is_list_of_str:
        raise ImproperlyConfigured("OPENWISP_ADMIN_THEME_CSS should be a list of strings.")
    is_list_of_str = all(isinstance(item, str) for item in openwisp_admin_js)
    if not isinstance(openwisp_admin_js, list) or not is_list_of_str:
        raise ImproperlyConfigured("OPENWISP_ADMIN_JS should be a list of strings.")
    return {
        'openwisp_admin_css': openwisp_admin_css,
        'openwisp_admin_js': openwisp_admin_js,
    }
