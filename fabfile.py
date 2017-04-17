from fabric.api import local, task


def hello(name):
    print('hello {}'.format(name))


def test():
    local('python --version')


def restart():
    local('sudo pkill gunicorn')
    local('sudo systemctl start gunicorn')
    local('sudo systemctl enable gunicorn')
    local('sudo systemctl restart nginx')


def reload_supervisord():
    local('supervisorctl stop all')
    local('sudo unlink /tmp/supervisor.sock')
    local('supervisord -c /home/ubuntu/supervisord.conf')
