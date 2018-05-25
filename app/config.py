import os
import configparser

BRAND_NAME = 'Falcon Message sender API'

inifile = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../conf/config.ini')
config = configparser.ConfigParser()
config.read(inifile)
