# # routers.py

class connectionRouter:
    # pass
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'connection':
            return 'default_mongo'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'connection':
            return 'default_mongo'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'connection' or obj2._meta.app_label == 'connection':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'connection':
            return db == 'default_mongo'
        return db == 'default'
