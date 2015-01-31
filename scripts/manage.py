import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.join(ROOT, 'src'))

command = sys.argv[1]

if command == "runserver":
    from promua.app import app
    app.run()
elif command == "syncdb":
    from promua.models import db
    db.create_all()
elif command == "shell":
    from IPython import embed
    embed()
else:
    sys.stderr.write("Unknown command: %s" % command)
