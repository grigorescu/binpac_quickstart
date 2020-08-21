# -*- coding: utf-8 -*-
#
import os
import sys

sys.path.insert(0, os.path.abspath('sphinxcontrib'))

extensions = ['zeek', 'sphinx.ext.githubpages', 'sphinx.ext.intersphinx']

intersphinx_mapping = {
    'zeek': ('https://docs.zeek.org/en/current', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# General information about the project.
project = u'External Use of Sensitive Protocols'
copyright = u'2020, ESnet'

version = u"source"

try:
    # Use the actual version if available
    with open('../VERSION', 'r') as f:
        version = f.readline().strip()
except:
    try:
        import git

        repo = git.Repo(os.path.abspath('.'))
        version = u"git/master"
        tag = [str(t) for t in repo.tags if t.commit == repo.head.commit]

        if tag:
            version = tag[0]

    except:
        pass

# The full version, including alpha/beta/rc tags.
release = version

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

highlight_language = 'zeek'

# -- Options for HTML output ---------------------------------------------------

import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'collapse_navigation': False,
    'display_version': True,
}

html_static_path = ['_static']

def setup(app):
    app.add_css_file("theme_overrides.css")
    from sphinx.highlighting import lexers
    from pygments.lexers.dsls import ZeekLexer
    lexers['zeek'] = ZeekLexer()

# Output file base name for HTML help builder.
htmlhelp_basename = 'zeek-pkg-docs'

# -- Options for todo plugin --------------------------------------------
todo_include_todos=True
