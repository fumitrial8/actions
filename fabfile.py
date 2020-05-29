from fabric.api import cd, env, run
import os.path

env.hosts = ['server']  # ~/.ssh/config で設定した、Hostをここに記入
env.ssh_config_path = '~/.ssh/config'
env.use_ssh_config = True

def deploy():
    BASE_DIR = '/home/ubuntu/'
    PIP = os.path.join(BASE_DIR, '.pyenv/shims/pip3')
    PYTHON = os.path.join(BASE_DIR, '.pyenv/shims/python3')
    GUNICORN = os.path.join(BASE_DIR, '.pyenv/shims/gunicorn')

    with cd(BASE_DIR):
        run('git pull origin master')

        run('{} install -U pip'.format(PIP))
        run('{} install -r requirements.txt'.format(PIP))

        run('{} -V'.format(PYTHON))
        run('{} manage.py migrate'.format(PYTHON))

        run('cp {} {}'.format(os.path.join(BASE_DIR, 'deploy', 'settings.py'),
                              os.path.join(BASE_DIR, 'django_application_server', 'settings.py')))  # DEBUGやDATABASEの設定を変更しておきたいので予め変更しておいたファイルを deploy ディレクトリにおいておきました。

        run('kill `cat gunicorn.pid`')
        run('{} django_application_server.wsgi:application -c gunicorn_conf.py'.format(GUNICORN))