netron_link = "https://netron.app"
cors_proxy = "https://cors.bridged.cc"
release_url = "https://github.com/larq/zoo/releases/download"


def html_format(source, language, css_class, options, md, **kwargs):
    return f'<div class="admonition abstract"><a class="netron-link" href="{netron_link}/?url={cors_proxy}/{release_url}/{source}"><p>Interactive architecture diagram</p></a></div>'
