from github import Github

# Github Enterprise with custom hostname
g = Github(base_url="https://github.enterprise/api/v3", login_or_token="<token>")

# Then play with your Github objects:
#for repo in g.get_user().get_repos():
#    print(repo.name)

org = g.get_organization("the-cool-boys")
for repo in org.get_repos():
    print(repo.name)

org.create_repo('hoge', description='hoge test', private=False, auto_init=False)