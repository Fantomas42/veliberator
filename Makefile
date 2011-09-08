# Makefile for Veliberator
#
# Aim to simplify development and release process
# Be sure you have run the buildout, before using this Makefile

NO_COLOR	= \033[0m
COLOR	 	= \033[32;01m
SUCCESS_COLOR	= \033[35;01m

all: kwalitee test docs clean package

package:
	@echo "$(COLOR)* Creating source package for Veliberator$(NO_COLOR)"
	@python setup.py sdist

test:
	@echo "$(COLOR)* Launching the tests suite$(NO_COLOR)"
	@./bin/test


docs:
	@echo "$(COLOR)* Generating Sphinx documentation$(NO_COLOR)"
	@./bin/docs

translations:
	@echo "$(COLOR)* Generating translation template$(NO_COLOR)"
	xgettext --language=Python --keyword=_ --from-code utf-8 --output=veliberator/locale/veliberator.pot ./veliberator/scripts/veliberator
	@echo "$(COLOR)* Merge the translations$(NO_COLOR)"
	msgmerge -o veliberator/locale/fr/LC_MESSAGES/veliberator.po veliberator/locale/fr/LC_MESSAGES/veliberator.po veliberator/locale/veliberator.pot

kwalitee:
	@echo "$(COLOR)* Running pyflakes$(NO_COLOR)"
	@./bin/pyflakes veliberator
	@echo "$(COLOR)* Running pep8$(NO_COLOR)"
	@./bin/pep8 --count -r veliberator
	@echo "$(SUCCESS_COLOR)* No kwalitee errors, Congratulations ! :)$(NO_COLOR)"

clean:
	@echo "$(COLOR)* Removing useless files$(NO_COLOR)"
	@find veliberator docs -type f \( -name "*.pyc" -o -name "\#*" -o -name "*~" \) -exec rm -f {} \;
	@rm -f \#* *~
	@rm -rf .tox
