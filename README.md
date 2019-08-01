# igo-scripts
Collection of scripts used by IGO

## Deployment
Deployments are organized by git branches. To deploy to a specific application, checkout the project and corresponding branch.

```
$ git clone https://github.com/mskcc/igo-scripts.git
Cloning into 'igo-scripts'...
remote: Enumerating objects: 23, done.
remote: Counting objects: 100% (23/23), done.
remote: Compressing objects: 100% (17/17), done.
remote: Total 23 (delta 3), reused 20 (delta 3), pack-reused 0
$ cd igo-scripts/
$ git checkout --track origin/MY_PROJECT    # Replace MY_PROJECT w/ desired application
```