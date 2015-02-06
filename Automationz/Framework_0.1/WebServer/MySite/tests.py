'''
Created on Dec 17, 2014

@author: sazid
'''
import unittest
from django.test import Client
from models import GetConnection #,GetData, GetColumnNames, GetQueryData

Conn = GetConnection()
cur = Conn.cursor()

class TestRemoveProfilePicture(unittest.TestCase):

    username = 'test_dummy'
    password = 'test'
    full_name = 'Test Dummy'
    profile_picture_name = 'test/picture.jpeg'

    def setUp(self):
        
        query = '''
        INSERT INTO user_info VALUES ('%s', '%s', '%s', '%s');
        ''' % (TestRemoveProfilePicture.username,
               TestRemoveProfilePicture.password, 
               TestRemoveProfilePicture.full_name,
               TestRemoveProfilePicture.profile_picture_name)
        
        cur.execute(query)


    def tearDown(self):
         
        query = '''
        DELETE FROM user_info WHERE username='%s' AND password='%s' AND full_name='%s';
        ''' % (TestRemoveProfilePicture.username,
               TestRemoveProfilePicture.password, 
               TestRemoveProfilePicture.full_name)
         
        cur.execute(query)
         
        Conn.close()


    def test_removal(self):
        c = Client()
        c.get('/Home/RemoveProfilePicture/', {'username': TestRemoveProfilePicture.username})
        
        query = '''
        SELECT profile_picture_name FROM user_info WHERE username='%s' AND password='%s' AND full_name='%s'
        ''' % (TestRemoveProfilePicture.username,
               TestRemoveProfilePicture.password, 
               TestRemoveProfilePicture.full_name)
        
        cur.execute(query)
        data = cur.fetchone()[0]
        self.assertEqual(data, TestRemoveProfilePicture.profile_picture_name,
                         'Should equal to %s' % TestRemoveProfilePicture.profile_picture_name)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()