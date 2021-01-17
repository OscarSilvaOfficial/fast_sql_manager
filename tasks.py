from invoke import task


@task
def build(c, docs=False):
    c.run('python setup.py sdist bdist_wheel')
    
@task
def push(c, docs=False):
    c.run('git add .')
    msg = input('Escreva a mensagem de commit: \n')
    c.run('git commit -m"{0}"'.format(msg))
    c.run('git push origin master')

@task
def uploadPypi(c, docs=False):
    c.run('twine upload --skip-existing dist/*')

@task
def deploy(c, docs=False):
    build()
    push()
    uploadPypi()