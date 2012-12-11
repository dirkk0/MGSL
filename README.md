# Minecraft Game Server Launcher


## Overview
This is the the Minecraft Game Server Launcher (MGSL). The MGSL is a series of scripts that can be used to launch a [Minecraft](minecraft.net) server in [Amazons EC2 cloud](http://aws.amazon.com) on an Ubuntu server.

(*As a matter of fact it is actually a xGSL because it can launch any game, that can be installed from the command line. If I think twice it is even a xySL because it is not limited to games. But we focus on minecraft here.*)

## What is does
The MGSL (once configured) is dead simply to use: you run 'python mgsl.py' once and the server starts and loads the your Minecraft world.

You run it again, and your world gets stored in a safe place and the server is terminated.

That's it.



## How it works

The MGSL is essentially a python script orchestrating a series of bash scripts that get executed one after another on a different machine. One challenge was the timing of the distinct steps and the detection of possible failures of these steps. The latter is not handled good enough yet to be honest, and is one of the main reasons why I hesitated to open source this. Then again: the whole service is working on a daily basis so it is fair to say that it works well enough to be useful.


## Installation
To run it, do a git clone of the project or download the zip file and unpack it.
You need to [install](http://stackoverflow.com/questions/2481287/how-do-i-install-boto) [boto](https://github.com/boto/boto):

    pip install boto

worked for me.

Then (important!) fill in these parameters in the file 'credentials.json' by copying the file 'credentials_template.json':

    cp credentials_template.json credentials.json

Then edit it with a text editor.

    {
    "AWS_ACCESS_KEY_ID": "AKIAXXXXXXXXXXXXQ5DA",
    "AWS_SECRET_ACCESS_KEY": "vDskXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX2cob",
    "key_name": "your-keypair",
    "key_path": "~/.ssh/",
    "ftp_server": "ftp://my.ftp.com/minecraft/",
    "ftp_username": "dirk",
    "ftp_password": "nowayjose"
    }

It is mandatory to fill in the first 4 lines. The first two parameters you find these in your [AWS Security Credentials settings](https://portal.aws.amazon.com/gp/aws/securityCredentials). The FTP lines are important if you want to make your world persistent.

## Why FTP?
Glad you are asking. Of course it would've been much more straightforward to save everything to Amazon S3, right? But then again, everybody and his brother has some FTP access lying around that is never really used. Since we don't deal with enterprise data this is good enough and usually doesn't cost any extra money. I guess I should add S3 anyways.

## Other solutions
I should mention that there are valid different system design decision possible, most notably a [DevOps](http://en.wikipedia.org/wiki/DevOps) solution based on [Chef](http://www.opscode.com/) or [Puppet](http://puppetlabs.com/). Also I should mention that there are various scripts out there that do similar things like [handle](http://forums.bukkit.org/threads/handle-control-your-bukkit-released-ver-0-3-0-stable.8605/), [McSuperServer](http://members.iinet.net.au/~paulone/mcsuperserver.html) and [Multicraft](http://www.multicraft.org/site/page?view=home).

## WARNING ...
I assume that people using this script *know what they are doing* and that Amazon charges *real money* for their servers. Use this script at your own risk! If you are new to Amazon EC2 you should get familiar with the services.

## ... but then again:
Having said that: you get a so-called 'free tier' if you register for AWS as a new customer. This means that you get 750h per month of the smallest EC2 instance (called 't1.micro') in the first year for free! Isn't that cool? This means that you can run one t1.micro instance 24/7.

**But:** this doesn't mean you can run several instances for free (which I mistakenly thought in the first place). Example: if you run two instances 24/7 you run 2 instances * 30 days * 24 hours = 1488 hours. But since the t1.micros are very cheap (around 0.02 Euro cent per hour) the remaining 1488-750=738 hours sum up to 14,76 Euros which probably won't max out your credit card either.

You usually want an 'm1.small' instance for more that three players, though.

Again: if you have access to the free tier, you can run your tests for free.


## Known issues ##

- bad login
This is not the scripts fault - for some reason there can be server timeouts on the minecraft.net site. You need to completely quit Minecraft and try again.

- time out
This when you try to connect too early. Just wait a minute and try again.

- no conection
This when you try to connect WAY too early. Or something went wrong.