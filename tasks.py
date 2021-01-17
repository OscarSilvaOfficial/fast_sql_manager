from invoke import task

@task
def deploy(c, docs=False):
    c.run('python setup.py sdist bdist_wheel')
    c.run('git add .')
    c.run('git commit -m"atualização da versão"')
    c.run('git push origin master')
    #c.run('twine upload --skip-existing dist/*')