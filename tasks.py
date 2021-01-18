import re
from invoke import task


def changeHotFix():
    filename = "setup.py"
    regex = r'[0-9]?[0-9].[0-9]?[0-9].[0-9]?[0-9]'

    with open(filename, 'r+') as f:
        text = f.read()
        subs = re.findall(regex, text)[0]  # 1.1.2
        reg = re.findall(r'.[0-9]?[0-9]', subs)[-1]  # .2

        res = re.sub(reg, f'.{str(int(reg.replace(".", ""))+1)}', subs)

        text = re.sub(subs, res, text)
        f.seek(0)
        f.write(text)
        f.truncate()

        print(f'HotFix alterado de {subs} para {res}')


def changeMinor():
    filename = "setup.py"
    regex = r'[0-9]?[0-9].[0-9]?[0-9].[0-9]?[0-9]'

    with open(filename, 'r+') as f:
        text = f.read()
        subs = re.findall(regex, text)[0]
        reg = r'.[0-9]?[0-9].'
        res = re.sub(
            reg,
            f".{str(int(re.findall(reg, subs)[0].replace('.', ''))+1)}.",
            subs)

        text = re.sub(subs, res, text)
        f.seek(0)
        f.write(text)
        f.truncate()

    print(f'Minor alterado de {subs} para {res}')


def changeMajor():
    filename = "setup.py"
    regex = r'[0-9]?[0-9].[0-9]?[0-9].[0-9]?[0-9]'

    with open(filename, 'r+') as f:
        text = f.read()
        subs = re.findall(regex, text)[0]  # 1.1.2
        reg = re.findall(r'[0-9]?[0-9].', subs)[0]  # .2

        res = re.sub(reg, f'{str(int(reg.replace(".", ""))+1)}.', subs)

        text = re.sub(subs, res, text)
        f.seek(0)
        f.write(text)
        f.truncate()

        print(f'Major alterado de {subs} para {res}')


@task
def build(c, docs=False):
    c.run('python setup.py sdist bdist_wheel')


@task
def push(c, docs=False):

    filename = "setup.py"
    regex = r'[0-9]?[0-9].[0-9]?[0-9].[0-9]?[0-9]'

    with open(filename, 'r+') as f:
        text = f.read()
        subs = re.findall(regex, text)[0]

    c.run('git add .')
    msg = input('Escreva a mensagem de commit: \n')
    c.run('git commit -m"{0}"'.format(msg))
    c.run('git tag -a {0} -m"New release"'.format(subs))
    c.run('git push origin {0}'.format(subs))


@task
def uploadPypi(c, docs=False):
    c.run('twine upload --skip-existing dist/*')


@task
def chooseManagementVersion(c, docs=False):
    version = input('Alterar [H-Hotfix | m-minor | M-Major]: ')

    if version == 'H':
        changeHotFix()
    if version == 'm':
        changeMinor()
    if version == 'M':
        changeMajor()


@task
def deploy(c, docs=False):
    c.run('inv chooseManagementVersion')
    c.run('inv build')
    c.run('inv push')
    c.run('inv uploadPypi')
