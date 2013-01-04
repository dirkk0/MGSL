from helpers import *
import os

credentials = json.load(open('credentials.json', 'r'))
app = json.load(open('app_minecraft.json', 'r'))

# this is the filename of the backup on the FTP server
# chose a simple word that will work as a filename

worldname = 'myworld'
# we assume that you entered the FTP credentials into
# credentials.json is you set the worldname
if credentials['ftp_server'] == 'fill_ftp_server':
    print "Warning: no FTP server available."
    print "If you want your world to be saved, you need to fill up the file 'credentials.json'."
    print "Continue, if you don't care and/or just testing."
    worldname = ''

# load all credetials

# we set back variables
generic_credentials = """
FTP_SERVER=%s
FTP_USERNAME=%s
FTP_PASSWORD=%s
FTP_FILE=%s
""" % (credentials['ftp_server'], credentials['ftp_username'], credentials['ftp_password'], worldname)

scripts = {}
for s in ['init', 'start', 'stop', 'save', 'load', 'new']:
    scripts[s] = open('scripts/%s.sh' % s, 'r').read()
    if worldname:
        scripts[s] = generic_credentials + scripts[s]


if __name__ == '__main__':

    if not do_test():
        print "Aborting."
        import sys
        sys.exit(0)

    if not os.path.exists('session.json'):
        a = raw_input("you are about to START a server. Continue? (y/n)")
        if a == "y":
            session = {}
            print worldname
            session["ip"], session["id"] = do_launch(app['type'], app['ami'], app['name'])
            open('session.json', 'w').write(json.dumps(session))
            print session

            if not os.path.exists(worldname + '.json'):
                # new world, create one
                for s in ['init', 'new', 'start']:
                    do_script(session['ip'], scripts[s])
            else:
                # existing world, load it
                print 'load'
                for s in ['init', 'load', 'start']:
                    do_script(session['ip'], scripts[s])

            print "You can now start minecraft and do a 'multiplayer/direct connect' to: " + session['ip']
            # print "To acess it do 'ssh -i %s/%s ubuntu@%s"
            # % (credentials['key_path'], credentials['key_name'], session['ip'])

    else:
        a = raw_input("you are about to END a server. Continue? (y/n)")
        if a == "y":
            session = json.load(open('session.json', 'r'))
            print session

            if worldname:
                for s in ['stop', 'save']:
                    do_script(session['ip'], scripts[s])
                open(worldname + '.json', 'w').write(json.dumps(session))

            do_kill(session['id'])
            os.remove('session.json')
