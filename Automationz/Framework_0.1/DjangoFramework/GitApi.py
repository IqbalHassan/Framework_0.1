import os


def pull_latest_git():
    try:
        g = git_repo()
        result = g.pull()
        print result 
        return result
    except Exception, e:
        print "There was an error while pulling the git changes: "
        print e
        return e
    
        
def git_repo():
    try:
        import git
        git_path =  str(os.path.dirname(os.path.realpath(__file__)).split("git")[0])+"git"+os.sep+"Framework_0.1"
        g = git.cmd.Git(git_path)
        return g
    except Exception, e:
        print "There was an error while pulling the git changes: "
        print e
        return e
    
    
def git_log(last_log = -3):
    try:
        g = git_repo()
        result = g.log(last_log)
        print result 
        return result
    except Exception, e:
        print "There was an error while pulling the git changes: "
        print e
        return e

#pull_latest_git()




#