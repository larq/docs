netron_link = "https://lutzroeder.github.io/netron"
cors_proxy = "https://cors-anywhere.herokuapp.com"
release_url = "https://github.com/larq/zoo/releases/download"


def html_format(source, language, css_class, options, md):
    return f'<div class="admonition abstract"><a class="netron-link" href="{netron_link}/?url={cors_proxy}/{release_url}/{source}"><p>Interactive architecture diagram</p></a></div>'
