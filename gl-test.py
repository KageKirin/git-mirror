from gitlab import Gitlab

# Gitlab or custom hostname
gl = Gitlab("https://gitlab.com", private_token="<token>")

print(gl)

gl.auth()
current_user = gl.user
print(current_user)
print(current_user.id)

print('make project')
p = gl.projects.create({'name': 'fgdfgdfg', 'user_id': str(current_user.id)})
print(p)

print('user info')
user = gl.users.get(current_user.id)

# Then play with your Gitlab objects:
# list all the projects
print('user projects')
for project in user.projects.list():
    print(project.name)


#org = g.get_organization("Arcana-dependencies")
#for repo in org.get_repos():
#    print(repo.name)
#
#org.create_repo('hoge', description='hoge test', private=False, auto_init=False)
