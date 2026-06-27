from core.ui import load_css, app_header


def page(title, subtitle=""):
    load_css()
    app_header(title, subtitle)
