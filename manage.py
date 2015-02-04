import sys

command = sys.argv[1]

if command == "runserver":
    from promua.views import app
    app.run()
elif command == "syncdb":
    from promua.models import db
    db.create_all()
elif command == "shell":
    from IPython import embed
    embed()
else:
    sys.stderr.write("Unknown command: %s" % command)
