import os
import sys

# Add project paths to sys.path
sys.path.insert(0, os.path.abspath("../../."))
sys.path.insert(0, os.path.abspath("../../modules"))
sys.path.insert(0, os.path.abspath("../../config"))

# Project Information
project = "Trailer Finder"
copyright = "2024, Kalibrado"
author = "Kalibrado"
release = "v1.5.8"

# General Configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.duration",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.imgconverter",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_markdown_builder",
    "recommonmark",
]

# Autodoc Options
autodoc_typehints = "description"  # Automatically extract typehints
autodoc_class_signature = "separated"  # Don't show class signature with the class' name
autodoc_member_order = "bysource"  # Order members by source order

# Source Suffix
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Autosummary Options
autosummary_generate = True  # Enable autosummary

# Paths
templates_path = ["_templates"]
exclude_patterns = ["_build", ".venv", "**/site-packages/**"]

# HTML Output Options
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

# HTML Theme Options
html_theme_options = {
    "logo": {
        "text": f"{project} {release}",
        "image": "logo.png"
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/kalibrado/trailer-finder",
            "icon": "fab fa-github",
            "type": "fontawesome",
        },
        {
            "name": "Reddit",
            "url": "https://www.reddit.com/user/Normal_Bike6536",
            "icon": "fab fa-reddit",
            "type": "fontawesome",
        },
        {
            "name": "Discord",
            "url": "https://discord.gg/kFdNCbnm",
            "icon": "fab fa-discord",
            "type": "fontawesome",
        },
    ],
    "show_prev_next": False,
}

# Intersphinx Mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# Todo Options
todo_include_todos = True  # Show todos in the output

# Napoleon Settings for Google and NumPy Style Docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
