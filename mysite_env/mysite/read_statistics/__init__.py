from os import  path

from  django.apps import  AppConfig

verbose_name="阅读计数"

def get_current_appname(file):
    return path.dirname(file).replace('\\','/').split('/')[-1]

class AppverbosenameConfig(AppConfig):
    name=get_current_appname(__file__)
    verbose_name=verbose_name

default_app_config=get_current_appname(__file__)+".__init__.AppverbosenameConfig"