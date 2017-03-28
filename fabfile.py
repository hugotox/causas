from fabric.api import local, task


def hello(name):
    print('hello {}'.format(name))


def test():
    local('python --version')
