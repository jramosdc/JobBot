#!/usr/bin/env python
from flaskext.script import Manager, Shell, Server
from weekly_employment_report import app

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())
manager.run()
