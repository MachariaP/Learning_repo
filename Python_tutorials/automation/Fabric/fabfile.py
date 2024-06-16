#!/usr/bin/env python3

from fabric import connection, config
from invoke import task

@task
def deploy(c):
    c.run('echo "Deploying..."')