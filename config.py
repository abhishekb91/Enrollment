import os


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or b'V\x8eoG\xb9\xbc;f\xa3FY<\xe4\xa9\x17\xa9\xcc\xc0i\xda'

    MONGODB_SETTINGS = {'db': 'UTA_Enrollment'}
