from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-a$&p^up8xwin6n+=%d2n0x!o@u$co-3042^a4%#w@p!$$b!ram'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
     'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Administrator',
    'products',
    'Seller',
    'Buyer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Full_Store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Full_Store.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'Full_Store.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'Administrator.User'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# jazzmin admin =======================

JAZZMIN_SETTINGS = {
    # ── BRANDING ──────────────────────────────────
    "site_title": "ShopHub Admin",
    "site_header": "ShopHub",
    "site_brand": "ShopHub",
    "site_logo": None,
    "login_logo": None,
    "welcome_sign": "Welcome to ShopHub Admin Panel",
    "copyright": "ShopHub © 2026",

    # ── TOP SEARCH ────────────────────────────────
    "search_model": ["Administrator.User", "products.Product", "Seller.Order"],

    # ── USER AVATAR ───────────────────────────────
    "user_avatar": None,

    # ── TOP MENU ──────────────────────────────────
    "topmenu_links": [
        {"name": "Home",      "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Storefront","url": "/",           "new_window": True},
        {"name": "Shop",      "url": "/shop/",      "new_window": True},
        {"model": "Administrator.User"},
        {"app": "products"},
    ],

    # ── USER MENU (top right) ─────────────────────
    "usermenu_links": [
        {"name": "Storefront", "url": "/", "new_window": True},
        {"model": "auth.user"},
    ],

    # ── SIDEBAR ───────────────────────────────────
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    "order_with_respect_to": [
        "Administrator",
        "products",
        "Seller",
        "Buyer",
        "auth",
    ],

    "icons": {
        "auth":                    "fas fa-users-cog",
        "auth.user":               "fas fa-user",
        "auth.Group":              "fas fa-users",
        "Administrator.User":      "fas fa-user-shield",
        "products.Product":        "fas fa-box-open",
        "products.Category":       "fas fa-tags",
        "Seller.Order":            "fas fa-shopping-bag",
        "Seller.OrderItem":        "fas fa-list",
        "Buyer.Wishlist":          "fas fa-heart",
    },

    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",

    # ── RELATED MODAL ─────────────────────────────
    "related_modal_active": True,

    # ── CUSTOM CSS / JS ───────────────────────────
    "custom_css": None,
    "custom_js":  None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,     # ← lets you tweak UI live in browser!

    # ── CHANGE VIEW ───────────────────────────────
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },

    # ── LANGUAGE CHOOSER ──────────────────────────
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,

    # ── COLOR THEME ───────────────────────────────
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,

    # ── SIDEBAR THEME ─────────────────────────────
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,

    # ── THEME ─────────────────────────────────────
    "theme": "darkly",        # choices: default, darkly, flatly, cosmo, superhero, etc.
    "dark_mode_theme": "darkly",

    # ── BUTTON CLASSES ────────────────────────────
    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success",
    },

    # ── ACTIONS ROW ───────────────────────────────
    "actions_sticky_top": True,
}