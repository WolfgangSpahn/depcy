# This is a Makefile for the project.

# Source files: *.py
MODULES   := .
SRC_DIR   := $(addprefix backend/,$(MODULES))
SRC       := $(foreach sdir,$(SRC_DIR),$(wildcard $(sdir)/*.py))

help:      ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e "s/\\$$//" | sed -e "s/##//"

install:   ## Install the project.
	python -m pip install -r .\requirements.txt

check:     ## Check code with pylint
	pylint --disable=all --enable=import-error,no-name-in-module,unresolved-import depcy

test:	   ## Run the tests.
test: $(SRC)
	python -m unittest test.flask.test_

source:    ## Show source files
	echo $(SRC)

doctest:   ## Run the doctests.
doctest: $(SRC)
	python -m depcy.merge
	# python -m depcy.string
	# python -m depcy.utils
	# python -m depcy.extract

# git-setup:  ## Initialize git repository.
# # setup a new git repository in the current directory.
# 	git init
# 	git add *
# 	git status
# 	git commit -m "initial commit"
# # add a new remote repository (named origin) to your local repository.
# 	git remote add origin https://github.com/WolfgangSpahn/depcy.git
# # rename the current branch to main (from master).
# 	git branch -M main
# # push the changes in your local repository to GitHub.
# 	git push -u origin main

# git-update: ## Update git repository.
# # add all the files in the current directory to the staging area.
# 	git add *
# # commit the changes to the staging area.
# 	git commit -m "update"
# # ammend the changes to the staging area. (if necessary)
# 	git commit --amend
# # push the changes in your local repository to GitHub.
# 	git push -u origin main
