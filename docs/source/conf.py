import os
import sys

sys.path.insert(0, os.path.abspath('../../.'))
sys.path.insert(0, os.path.abspath('../../modules'))
sys.path.insert(0, os.path.abspath('../../config'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = "Trailer Finder"
copyright = "2024, Kalibrado"
author = "Kalibrado"
release = "v1.5.8"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.githubpages",
    "sphinx.ext.autosummary",
]

autosummary_generate = True
templates_path = ["_templates"]
exclude_patterns = ["_build", ".venv", "**/site-packages/**"]

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]
