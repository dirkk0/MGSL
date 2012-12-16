import subprocess
import time

# import db

import urllib
import urllib2


from boto import ec2

import json


def do_wait():
    time.sleep(0.2)


def do_ssh(ip, cmd):
    user = "ubuntu"

    credentials = json.load(open('credentials.json', 'r'))
    key_path = credentials['key_path']
    key_name = credentials['key_name']

    args = "-i " + key_path + key_name
    args += " -o StrictHostKeyChecking=no"

    process = subprocess.Popen("ssh %s %s@%s '%s'" % (args, user, ip, cmd), shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, stderr = process.communicate()
    process.poll()
    return output


def do_wait2(ip):
    print 'waiting for machine to be ready ...'
    output = do_ssh(ip, "ls")
    while output[-9:-2] == 'refused':
        # print output
        print '.',
        output = do_ssh(ip, "ls")
        time.sleep(2)
    print "... succesfully logged in once."


def do_script(ip, script):
    verbose = 1
    for line in script.split("\r\n"):
        if verbose:
            print line
        if line:
            output = do_ssh(ip, line.decode('string_escape'))
            if verbose:
                print output

def do_launch(it, instance_name):

    test = False
    ami = "ami-137bcf7a"

    credentials = json.load(open('credentials.json', 'r'))
    ec2c = ec2.connection.EC2Connection(
           credentials['AWS_ACCESS_KEY_ID'],
           credentials['AWS_SECRET_ACCESS_KEY'])

    user_data = """#!/bin/bash
                touch test.txt
                """

    if not test:
        group_name = "mgsl"
        security_group = do_security_group(ec2c, group_name)
        key_name = credentials['key_name']

        reservation = ec2c.run_instances(ami,
                                          instance_type=it,
                                          key_name=key_name,
                                          user_data=user_data,
                                          security_groups=[security_group])

        print "waiting for reservation to finish ..."
        for r in ec2c.get_all_instances():
            if r.id == reservation.id:
                break
        i = reservation.instances[-1]
        print "...finished."

        ec2c.create_tags([i.id], {"Name": instance_name})

        print "waiting for AMI to start ..."
        while not i.update() == 'running':
            print ".",
            time.sleep(2)
        print " ... success!"
        print i.ip_address
        print i.id

        do_wait2(i.ip_address)

        return (i.ip_address, i.id)
    else:
        print 'just testing'
        print instance_name


def do_kill(id):
    credentials = json.load(open('credentials.json', 'r'))
    ec2c = ec2.connection.EC2Connection(
           credentials['AWS_ACCESS_KEY_ID'],
           credentials['AWS_SECRET_ACCESS_KEY'])

    print "Trying to terminate %s ... " % id
    r = ec2c.get_all_instances(filters={'instance-id': id})
    r[0].instances[0].terminate()
    print "... terminated %s." % id


def do_killall():
    credentials = json.load(open('credentials.json', 'r'))
    ec2c = ec2.connection.EC2Connection(
           credentials['AWS_ACCESS_KEY_ID'],
           credentials['AWS_SECRET_ACCESS_KEY'])

    instances = ec2c.get_all_instances()

    if instances:
        for r in instances:
            i = r.instances[0]

            if i.__dict__['tags']:
                name = i.__dict__['tags']['Name']
            ip = i.public_dns_name
            state = i.state
            if state == 'running':
                print name, ip, state
                print "you are about to kill", name, i.id
                a = raw_input()
                if a == "y":
                    print "kill"
                    print i.terminate()
                else:
                    print "abort - no kill"


def do_status():
    credentials = json.load(open('credentials.json', 'r'))
    ec2c = ec2.connection.EC2Connection(
           credentials['AWS_ACCESS_KEY_ID'],
           credentials['AWS_SECRET_ACCESS_KEY'])

    instances = ec2c.get_all_instances()

    if instances:
        for r in instances:
            i = r.instances[0]

            if i.__dict__['tags']:
                name = i.__dict__['tags']['Name']
            ip = i.public_dns_name
            state = i.state
            print name, ip, state
    else:
        print 'no servers running.'


def do_dns1(hostname, ip):
    for i in xrange(5):
        result = do_dns2(hostname, ip)
        if result:
            return
        else:
            print 'dns failed %i' % i
            time.sleep(1)


def do_dns2(hostname, ip):
    credentials = json.load(open('credentials.json', 'r'))

    data = {}
    data['hostname'] = hostname
    data['myip'] = ip
    print data
    url_values = urllib.urlencode(data)
    url = 'http://members.dyndns.org:8245/nic/update'
    full_url = url + '?' + url_values
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None,
                              url,
                              credentials['dyn_username'],
                              credentials['dyn_password'])
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    try:
        result = opener.open(full_url)
        print result.read()
        return True
    except:
        print "fail!"
        return False


def do_security_group(ec2c, group_name):
    try:
        group = ec2c.get_all_security_groups(groupnames=[group_name])[0]
    except ec2c.ResponseError, e:
        if e.code == 'InvalidGroup.NotFound':
            print "creating group %s" % group_name
            group = ec2c.create_security_group(group_name, group_name)

            ports = [
                      ['icmp', '-1', '-1'],
                      ['tcp', '22', '22'],
                      ['tcp', '25565', '25565'],
                      ['udp', '25565', '25565'],
                    ]

            for port in ports:
                ec2c.authorize_security_group(group_name,
                               ip_protocol=port[0],
                               from_port=port[1],
                               to_port=port[2],
                               cidr_ip='0.0.0.0/0')
                print port
    return group


def do_test():
    credentials = json.load(open('credentials.json', 'r'))

    success = True
    for s in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'key_name', 'key_path']:
        # print credentials[s], s, credentials[s] == s
        if credentials[s] == s:
            print "You need to edit credetials.json and fill in the " + s
            success = False
    return success
