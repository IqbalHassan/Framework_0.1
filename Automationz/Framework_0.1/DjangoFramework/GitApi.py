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
        user_name = os.getenv('USERNAME')
        g = git.cmd.Git("C:\Users\%s\git\Framework_0.1"%user_name)
        return g
    except Exception, e:
        print "There was an error while pulling the git changes: "
        print e
        return e
    
    
def git_log(last_log = -10):
    try:
        g = git_repo()
        result = g.log(last_log)
        print result 
        return result
    except Exception, e:
        print "There was an error while pulling the git changes: "
        print e
        return e
