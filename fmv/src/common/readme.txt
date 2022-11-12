
Every module uses this common repo, must run the following command once.
    git submodule add git@github.com:Savvly/common.git common
    git commit -a -m "added common as a submodule"
    git push

The repo that uses the common repo, must run the following command every time that common is changed:
    git submodule update --recursive --remote