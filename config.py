import os


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or "asjdbas6d967toyeb21lpdy0fyasdlsjh"

    MONGODB_SETTINGS = {'db': 'UTA_Enrollment'}
