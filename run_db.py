import sys

import run_db_data
import run_db_mutator
from db.database import SQLALCHEMY_DATABASE_URL, engine


class Command:
    def __init__(self, action, does=""):
        self.action = action
        self.does = does


def connection_string():
    print("Db Connection String: \t" + SQLALCHEMY_DATABASE_URL)
    print(engine.pool.status())


def close():
    print(engine.dispose())


def data():
    run_db_data.add_master_data()


def auto():
    run_db_mutator.drop_db_version()
    run_db_mutator.remove_local_migrations()
    run_db_mutator.create_migration()
    run_db_mutator.apply_migations()
    data()


def scratch():
    run_db_mutator.drop_all()
    run_db_mutator.drop_db_version()


def help():
    for name, value in switch().items():
        # print(name +"\t \t" +value.does)
        print("{0:20} {1}".format(name, value.does))


def unknown():
    print("Unknown command argument, see 'python run_db.py help'")


def has_model_changes():
    print(run_db_mutator.has_model_changes())


def add_migration_and_update():
    if run_db_mutator.has_model_changes():
        run_db_mutator.create_migration()
        run_db_mutator.apply_migations()


def switch():
    switcher = {
        "connection": Command(connection_string, "show current connection string"),
        "close": Command(close, "close all connection"),
        "drop": Command(run_db_mutator.scratch, "drop alembic_version table and all alembic created objects"),
        "auto": Command(auto,
                        "drop alembic_version table, remove migration files, create migration & update db, add master datas"),

        "data": Command(data, "add master datas"),
        "remove-version-files": Command(run_db_mutator.remove_local_migrations, "remove local migration files"),
        "drop-version-table": Command(run_db_mutator.drop_db_version, "drop alembic_version table"),
        "update": Command(run_db_mutator.apply_migations, "apply current migraion files to db"),

        "help": Command(help, "show avaiable commands")
    }
    return switcher


if __name__ == "__main__":
    command = ""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

    switcher = switch()
    item = switcher.get(command, Command(unknown, ""))
    print(item.does)
    item.action()
