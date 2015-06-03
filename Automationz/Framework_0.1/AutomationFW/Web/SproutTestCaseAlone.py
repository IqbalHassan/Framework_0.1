__author__ = 'Raju'
import sys
from Web.SproutSupport import *
def LoginTestCase():
    BrowserSelection('Firefox')
    OpenLink('https://sproutqa.sproutatwork.com')
    Login('hossain.iqbal@gmail.com','teamWork','Riz')
    Tear_Down()
def main():
    LoginTestCase()

if __name__=='__main__':
    main()