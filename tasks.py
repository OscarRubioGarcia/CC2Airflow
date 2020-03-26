import sys
import time

from invoke import task


@task
def active(ctx):
    print("Invoke is Active!")


@task
def testApi(ctx):
    ctx.run("python -m unittest tests/unittests.py")


@task
def runGunicorn(ctx, port="5000"):
    if port == "DEFAULT":
        port = 5000
        ctx.run("gunicorn -b 0.0.0.0:%s \"app:app\" " % port)
    else:
        ctx.run("gunicorn -b 0.0.0.0:%s \"app:app\" " % port)


@task(help={'port': "Port number that waitress will use when deploying the microservice. (Usable for Windows)"})
def callWaitress(ctx, port="5000"):
    if port == "DEFAULT":
        port = 5000
        ctx.run("waitress-serve --port=%s app:app" % port)
    else:
        ctx.run("waitress-serve --port=%s app:app" % port)