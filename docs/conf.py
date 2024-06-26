# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import pathlib
import sys
from pkg_resources import get_distribution

print("python exec:", sys.executable)
print("sys.path:", sys.path)
root = pathlib.Path(__file__).parent.parent.absolute()
os.environ["PYTHONPATH"] = str(root)
sys.path.insert(0, str(root))

# import enjoy_slurm  # isort:skip

# -- Project information -----------------------------------------------------

project = "enjoy-slurm"
copyright = "2021, Lars Buntemeyer"
author = "Lars Buntemeyer"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
# see https://pypi.org/project/setuptools-scm/ for details

release = get_distribution("enjoy_slurm").version
# for example take major/minor
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "nbsphinx",
    #   "recommonmark",
    "sphinx.ext.mathjax",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "numpydoc",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "sphinxcontrib.srclinks",
]

extlinks = {
    "issue": ("https://github.com/larsbuntemeyer/enjoy-slurm/issues/%s", "#%s"),
    "pr": ("https://github.com/larsbuntemeyer/enjoy-slurm/pull/%s", "#%s"),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "**.ipynb_checkpoints", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "pangeo"
# html_theme = "sphinx_book_theme"
html_theme = "furo"
html_title = "enjoy-slurm"

# html_theme_options = dict(
#    repository_url="https://github.com/larsbuntemeyer/enjoy-slurm",
#    repository_branch="main",
#    path_to_docs="docs",
#    use_edit_page_button=True,
#    use_repository_button=True,
#    use_issues_button=True,
#    home_page_in_toc=False,
#    extra_navbar="",
#    navbar_footer_text="",
# )

css_vars = {
    "admonition-font-size": "0.9rem",
    "font-size--small": "92%",
    "font-size--small--2": "87.5%",
}
html_theme_options = dict(
    source_repository="https://github.com/larsbuntemeyer/enjoy-slurm",
    source_branch="main",
    sidebar_hide_name=False,
    source_directory="docs/",
    light_css_variables=css_vars,
    dark_css_variables=css_vars,
)

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]
html_static_path = []


# -- nbsphinx specific options ----------------------------------------------
# this allows notebooks to be run even if they produce errors.
nbsphinx_allow_errors = True


autosummary_generate = True

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,
}
napoleon_use_param = True
napoleon_use_rtype = True

numpydoc_show_class_members = False
# numpydoc_validation_checks = {"all"}
