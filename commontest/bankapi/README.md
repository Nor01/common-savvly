# bankapi
API to do bank operations

The common Git Submodule
-------------------------
Run Once:
---------
    git submodule add git@github.com:Savvly/common.git common
    git commit -a -m "added common as a submodule"
    git push

Runs every time Common is changed:
----------------------------------
	git submodule update --recursive --remote
	git commit -m "Updated common submodule"
	git push

