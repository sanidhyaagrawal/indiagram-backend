
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import re


# -*- coding: utf-8 -*-

"""
List of reserved usernames (pre-defined list of special banned and reserved keywords in names,
such as "root", "www", "admin"). Useful when creating public systems, where users can choose
a login name or a sub-domain name.
__References:__
1. http://www.bannedwordlist.com/
2. http://blog.postbit.com/reserved-username-list.html
3. https://ldpreload.com/blog/names-to-reserve
"""

_d = """
about
abuse
access
account
accounts
add
address
adm
admin
administration
administrator
adult
advertising
affiliate
affiliates
ajax
anal
analytics
android
anon
anonymous
anus
api
app
apps
archive
arse
ass
atom
auth
authentication
autoconfig
avatar
backup
balls
ballsack
banner
banners
bastard
biatch
billing
bin
bitch
blog
blogs
bloody
blowjob
board
bollock
bollok
boner
boob
bot
bots
broadcasthost
bugger
bum
business
butt
buttplug
cache
cadastro
calendar
campaign
careers
cgi
chat
client
cliente
clitoris
cock
code
comercial
compare
compras
config
connect
contact
contest
coon
copyright
crap
create
css
cunt
damn
dashboard
data
db
delete
demo
design
designer
dev
devel
dick
dildo
dir
directory
doc
docs
domain
download
downloads
dyke
ecommerce
edit
editor
email
end
errors
events
example
fag
faq
faqs
favorite
feck
feed
feedback
felching
fellate
fellatio
file
files
flange
flog
follow
forum
forums
free
ftp
fuck
fucker
fudge
fudgepacker
gadget
gadgets
games
god
goddamn
group
groups
guarantee
guest
guests
hell
help
home
homepage
homo
host
hosting
hostmaster
hostname
hpg
html
http
httpd
https
image
images
imap
img
index
indice
info
information
inquiry
intranet
intro
introduction
invite
ipad
iphone
irc
is
isatap
it
java
javascript
jerk
jizz
job
jobs
js
knob
knobend
knowledgebase
labia
licensing
links
list
lists
lmao
lmfao
localdomain
localhost
log
login
logout
logs
magazine
mail
mail1
mail2
mail3
mail4
mail5
mailer
mailer-daemon
mailing
manager
marketing
master
me
media
message
messenger
microblog
microblogs
mine
mis
mob
mobile
motherfucker
movie
movies
mp3
msg
msn
muff
music
musicas
mx
my
mysql
name
named
net
network
new
news
newsletter
nick
nickname
nigga
nigger
no-reply
nobody
noc
noreply
notes
noticias
ns
ns1
ns2
ns3
ns4
old
omg
online
operator
order
orders
packer
page
pager
pages
panel
password
payments
penis
perl
photo
photoalbum
photos
php
pic
pics
piss
plugin
plugins
policies
policy
poop
pop
pop3
post
postfix
postmaster
posts
pricing
prick
privacy
profile
project
projects
promo
pub
pube
public
pussy
python
queer
random
refund
refunds
register
registration
return
returns
reviews
root
rss
ruby
sale
sales
sample
samples
script
scripts
scrotum
search
secure
security
send
service
services
setting
settings
setup
sex
sh1t
shit
shop
signin
signup
site
sitemap
sites
slut
smegma
smtp
soporte
spunk
sql
ssh
ssladmin
ssladministrator
sslwebmaster
stage
staging
start
stat
static
stats
status
store
stores
subdomain
subscribe
suporte
support
survey
sysadmin
system
tablet
tablets
talk
task
tasks
tech
telnet
terms
test
test1
test2
test3
teste
testimonials
tests
theme
themes
tit
tmp
todo
tools
tosser
tour
turd
tv
twat
update
upload
url
usage
usenet
user
username
users
usuario
uucp
vagina
vendas
video
videos
visitor
wank
web
webmail
webmaster
website
websites
whore
win
workshop
wpad
wtf
ww
wws
www
www1
www2
www3
www4
www5
www6
www7
wwws
wwww
xpg
xxx
you
yourdomain
yourname
yoursite
yourusername
"""

username_regex = re.compile(
    r"""
    ^                       # beginning of string
    (?!_$)                  # no only _
    (?![-.])                # no - or . at the beginning
    (?![0-9]$)               # no only numbers
    (?!.*[.]{2})            # no __ or _. or ._ or .. or -- inside
    [a-zA-Z0-9_.]+          # allowed characters, atleast one must be present
    (?<![.-])               # no - or . at the end
    $                       # end of string
    """,
    re.X,
)

trailing_periods_regex = re.compile(
    r"""
    ^                       # beginning of string
    (?!.*[-.]{2})            # no __ or _. or ._ or .. or -- inside
    $                       # end of string
    """,
    re.X,
)

periods_at_end_regex = re.compile(
    r"""
    ^                       # beginning of string
        (?<![.-])               # no - or . at the end
    $                       # end of string
    """,
    re.X,
)

periods_in_starting_regex = re.compile(
    r"""
    ^                       # beginning of string
    (?![-.])                # no - or . at the beginning
    $                       # end of string
    """,
    re.X,
)

only_numbers__regex = re.compile(
    r"""
    ^                       # beginning of string
    (?![0-9]$)               # no only numbers
    $                       # end of string
    """,
    re.X,
)


def is_safe_username(
        username, whitelist=[], blacklist=[], regex=username_regex, max_length=30, min_length=3):
    print(username)
    if max_length and len(username) > max_length:
        return(False, 'Enter a name under 30 characters.')

    if min_length and len(username) < min_length:
        return(False, 'The username {} is not available'.format(username))

    elif username.find("..") >= 0:
        return(False, "You can't have more than one period in a row.")

    elif username[0] == '.':
        return(False, "You can't start your username with a period.")

    elif username[-1] == '.':
        return(False, "You can't end your username with a period.")

    elif username.isnumeric():
        return(False, "Your username cannot contain only numbers.")

    elif not re.match(regex, username):
        return(False, 'Username can only use letters numbers underscores and periods.')

    wordlist = get_reserved_wordlist()
    whitelist = set([each_whitelisted_name.lower()
                     for each_whitelisted_name in whitelist])
    blacklist = set([each_blacklisted_name.lower()
                     for each_blacklisted_name in blacklist])
    wordlist = wordlist - whitelist
    wordlist = wordlist.union(blacklist)

    return (False, 'The username {} is not available'.format(username)) if username.lower() in wordlist else (True, 'Available')


def get_reserved_wordlist():
    return set(_d.splitlines())


__all__ = ["get_reserved_wordlist"]


existing = ['indiagram', 'sanidhya69', "vansh", "rohan"]


def isavailable(username):
    if username in existing:
        return(False)
    else:
        return(True)


def try_addto_available(username, available):
    if isavailable(username):
        available.append(username)
    return(available)


def getavailable(username, available):
    if len(username) > 5:
        center = round(len(username)/2)
        temp = username[: center] + '_' + username[center:]
        available = try_addto_available(temp, available)

        temp = username[: center] + '.' + username[center:]
        available = try_addto_available(temp, available)

        temp = username[: center-1] + '_' + username[center-1:]
        available = try_addto_available(temp, available)

        temp = username[: center-1] + '.' + username[center-1:]
        available = try_addto_available(temp, available)

        temp = username[: center-2] + '_' + username[center-2:]
        available = try_addto_available(temp, available)

        temp = username[: center-2] + '.' + username[center-2:]
        available = try_addto_available(temp, available)
        while len(available) != 10:
            temp = username + str(random.randint(1, 999))
            available = try_addto_available(temp, available)
    else:
        while len(available) != 10:
            temp = username + str(random.randint(1, 999))
            available = try_addto_available(temp, available)
    return(available)


def custom_mordifications(username, available):
    available = try_addto_available(username, available)

    username = username+'x'
    available = try_addto_available(username, available)

    # username = username.replace("a", "")
    # available = try_addto_available(username, available)

    return(available)

# returns True if username available
# returns False if username NOT available, returns also list of available suggestions
# returns None if username not safe/invalid regex


def check_or_get_username(username):
    _isvalid, reason = is_safe_username(username)
    if _isvalid:
        if not isavailable(username):
            available = []
            username = username.replace(".", "")
            username = username.replace("_", "")
            ###
            available = custom_mordifications(username, available)
            available = getavailable(username, available)

            return(False, available)
        else:
            return(True, 'Username Available')
    else:
        return(None, reason)


check_or_get_username("username")
