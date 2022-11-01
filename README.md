<h1 align="center"> bulk-pr-creator </h1><br>

## _Table of Contents_

- [Introduction](#introduction)
- [How to run](#how-to-run)
- [Templates](#templates)
- [Postscript](#postscript)

## _Introduction_

_The **bulk-pr-creator** it is a lightweight and portable tool for changing multiple repositories at once._

_The aim of the project is to be automatizing the massive changes of repositories with yaml files._

## _How to run_

_You have two options for using tool **locally** and with **GitHub** **actions**._

### _Locally_

_At the first you should install some **dependencies** :_

_**Install python with**_ [**_brew_**](https://brew.sh/#install)  :

```
$ brew install python
```

**_Install python libraries from ```requirements.txt``` :_**

```
$ pip install -r requirements.txt
```

**_Install_** [**_GitHub CLI_**](https://cli.github.com/) :

```
$ brew install gh
```

**_Run script_** :

```
$ python ./script/main.py <filename> {<org> | <username>} <token>
```

***Params*** :

> ```<filename>``` name of the yml \
> Please provide file name  **without** extension

> ```<org>``` name of organization in which repo located

> ```<username>``` name of user in which repo located

> ```<token>``` personal access token of
>user ([How to create PAT?](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)) \
> Please be sure that you'd grant **right** scope to token

### _With GitHub actions_

**_For using this tool you should set 2 secrets in GitHub_**
**_repo_** ([How to set secret?](https://docs.github.com/en/actions/security-guides/encrypted-secrets)) :

> ```GH_ORG``` name of organization (or username of user) in which repo located

> ```GH_TOKEN``` personal access token of
>user ([How to create PAT?](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)) \
> Please be sure that you'd grant **right** scope to token

**_Add command to ```apply.sh``` file_** :

```
$ python ./script/main.py <filename> 
```

***Params*** :
> ```<filename>``` name of the yml \
> Please provide file name  **without** extension

## _Templates_

**_There are 3 type of actions:_**

**_EDIT_**:

_**The edit action changes file, commit and push changes to GitHub.**_

```YML file:```
```yaml
bulk:
  edit:
    files:
      - path: <path the file in ms which will be edited>
        changes:
          - from: <what to change>
            to: <change to>
          - from: <what to change>
            to: <change to>
      - path: <path the file in ms which will be edited>
        changes:
          - from: <what to change>
            to: <change to>
          - from: <what to change>
            to: <change to>
    github:
      branch: <branch-name>
      commit: <commit-name>
      cancel:
        pipeline: <true if you want to cancel the pipeline otherwise false >
    repos: <name of repo list with extension>

```

**_CREATE_**:

**_The creation action copies defined file to path destination in MS, then commit and push changes to GitHub._**

```YML file:```
```yaml
bulk:
  create:
    files:
      - filename: <file name with extension>
        destination : <destination of file>
      - filename: <file name with extension>
        destination: <destination of file>
    github:
      branch: <branch name>
      commit: <commit name>
      cancel:
        pipeline: <true if you want to cancel the pipeline otherwise false >
    repos: <name of repo list with extension>
```

**_PR creating_**:

**_The PR action creates PR from X branch to Y branch._**

```YML file:```
```yaml
bulk:
  pr:
    from: <branch-name which from creating pr>
    to: <pr to branch-name>
    name: <PR-name>
    body: <PR-body>
    assignee: <Assign pr to people by their login. Use "@me" to self-assign.>
    cancel:
      pipeline: <true if you want to cancel the pipeline otherwise false >
    repos: <name of repo list with extension>
```
**_Combining yml-s_**:

_**You can also combine this actions in one yml file**_ :

```YML file:```
```yaml
bulk:
  edit:
    files:
      - path: <path the file in ms which will be edited>
        changes:
          - from: <what to change>
            to: <change to>
          - from: <what to change>
            to: <change to>
      - path: <path the file in ms which will be edited>
        changes:
          - from: <what to change>
            to: <change to>
          - from: <what to change>
            to: <change to>
    github:
      branch: <branch-name>
      commit: <commit-name>
      cancel:
        pipeline: <true if you want to cancel the pipeline otherwise false >
    repos: <name of repo list with extension>
  create:
    files:
      - filename: <file name with extension>
        destination : <destination of file>
      - filename: <file name with extension>
        destination: <destination of file>
    github:
      branch: <branch name>
      commit: <commit name>
      cancel:
        pipeline: <true if you want to cancel the pipeline otherwise false >
    repos: <name of repo list with extension>
  pr:
    from: <branch-name which from creating pr>
    to: <pr to branch-name>
    name: <PR-name>
    body: <PR-body>
    assignee: <Assign pr to people by their login. Use "@me" to self-assign.>
    cancel:
      pipeline: <true if you want to cancel the pipeline otherwise false >
    repos: <name of repo list with extension>
```

## _Postscript_

**_Files locations:_**

- ```yml``` files should be placed in ```changelog``` folder 
- ```files``` which contains  _**repo names**_ should be places in ```repo_list``` folder
- ```files``` for create action should be placed in ```changelog/files``` folder



**_About PAT:_**

After each run of GitHub actions ```GH_TOKEN```  secret value is reset. This is done for security reasons. You can turn
off this step by commenting   ```"Updating GitHub PAT from secret to null"``` step in pipeline.

**_Self-preservation_**

Please comment all commands in ```apply.sh``` to avoid unwanted execution 
