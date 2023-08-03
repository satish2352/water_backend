from django.apps import AppConfig



class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iwater'


#-------------- Under function is used for scheduler start in jobs folder-------------------------
    def ready(self):             
      from iwater.jobs import updater
      updater.start()
