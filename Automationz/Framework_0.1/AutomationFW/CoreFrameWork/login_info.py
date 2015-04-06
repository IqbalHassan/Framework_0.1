import sys
import Global
sys.path.append("..")
def get_ip(environment):
    if environment=='Production':
        return '135.23.123.206'
    if environment=='Test':
        return '127.0.0.1'
    
username='iqbal_hassan'
password='iqbal_hassan'
project='AscendLearning'
team='ClickSafety'
server=get_ip(Global.Environment)
port=5432


#dataBaseConfig

database_name='postgres'
superuser='postgres'
super_password='password'


