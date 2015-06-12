__author__ = 'Raju'
from AutomationFW.CoreFrameWork import FileUtilities
import ConfigParser
import os

def write_config_file(full_file_name,method,run_id,steps_data,default_configs,klass):
    config_file_name=full_file_name+os.sep+'ConfigFiles'+os.sep+klass+'.conf'
    result_file_path=full_file_name+os.sep+'Result'+os.sep+run_id.replace(':','-')+'.xml'#full_file_name+os.sep+'Result'+os.sep+run_id+'.xml'
    log_file_path=full_file_name+os.sep+'Log'+os.sep+run_id.replace(':','-')+'.log'#full_file_name+os.sep+'Log'+os.sep+run_id+'.log'
    config_parser=ConfigParser.ConfigParser()
    config_parser.read(config_file_name)
    if method not in config_parser.sections():
        config_parser.add_section(method)
        config_parser.set(method,'description','Default Description of this section.(can be overridden)')
    #give the data in the
    steps_data=steps_data[0]
    for each in steps_data:
        key=each[0]
        value=each[1]
        print method,key,value
        config_parser.set(method,key,value)
    for each in default_configs:
        if each not in config_parser.sections():
            config_parser.add_section(each)
        setting=default_configs[each]
        for eachtime in setting:
            config_parser.set(each,eachtime[0],eachtime[1])
    #override the log file
    config_parser.set('bench','result_path',result_file_path)
    config_parser.set('bench','log_path',log_file_path)
    FileUtilities.CreateFolder(full_file_name+os.sep+'ConfigFiles',False)
    with(open(config_file_name,'w')) as open_file:
        config_parser.write(open_file)
    open_file.close()
