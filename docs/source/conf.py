# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath("../../"))

# -- Project information -------------------------------------------------------
project = "Django CMS Taxonomy"
copyright = "2026, Florian Braun"
author = "Florian Braun"
release = "0.1.0"

# -- General configuration -------------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output ---------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "sidebar_hide_name": False,
    "light_css_variables": {
        "color-brand-primary": "#0066cc",
        "color-brand-content": "#0066cc",
    },
}

# MyST configuration
myst_enable_extensions = [
    "colon_fence",
    "linkify",
]

# -- Autodoc configuration ----------------------------------------------------
autodoc_typehints = "description"
autodoc_member_order = "bysource"
