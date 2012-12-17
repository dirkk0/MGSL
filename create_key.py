from helpers import *
import os

if __name__ == '__main__':
    key_name = 'mgsl'
    key_dir = os.path.expanduser('~/.ssh/')
    key_extension = '.pem'

    key_path = os.path.join(key_dir, key_name + key_extension)
    if os.path.exists(key_path):
        print 'key already exists at ' + key_path
    else:
        print 'creating ' + key_path + '...'
        credentials = json.load(open('credentials.json', 'r'))
        ec2c = ec2.connection.EC2Connection(
            credentials['AWS_ACCESS_KEY_ID'],
            credentials['AWS_SECRET_ACCESS_KEY'])

        do_createKey(ec2c, key_name)
        print '...done.'
