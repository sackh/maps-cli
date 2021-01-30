export DEST=docs/source
rm -rf $DEST/_build
rm -rf $DEST/_static
rm -rf $DEST/_templates

# Just creating conf.py, Makefile and make.bat once, hence commenting below.
#sphinx-quickstart --quiet --author Sachin Kharude --project maps\
#	--ext-coverage --ext-autodoc --ext-viewcode --ext-doctest \
#	--extensions sphinx_autodoc_typehints \
#	$DEST
sphinx-apidoc --private --separate --module-first --full -o $DEST maps
sphinx-build -b html -D html_theme=sphinx_rtd_theme $DEST $DEST/_build/html