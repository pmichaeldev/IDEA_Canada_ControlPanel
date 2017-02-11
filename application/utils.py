from werkzeug import generate_password_hash, check_password_hash
from hmac import new
from database import app
from datetime import datetime
import re

__dateformat__ = "%B, %d %Y"
SECRET = app.config['SECRET_KEY']
hash_method = "sha256"

# returns a list in the form of [salt, hash]
def get_salt_hash(h):
    if h:
        return h.split("$")[1:3]

def gen_hash(password):
    return generate_password_hash(password, method=hash_method, salt_length=16)

def check_password(h, salt, password):
    if not h or not salt or not password:
        return False
    else:
        h = hash_method + '$' + salt + '$' + h
        return check_password_hash(h, password)

# Checks to see if the given first name is valid
FIRST_NAME_RE = re.compile(r"^[a-zA-Z]{2,16}")
def valid_first_name(name):
    return name and FIRST_NAME_RE.match(name)

LAST_NAME_RE = re.compile(r"^[a-zA-Z]{2,16}")
def valid_last_name(name):
    return name and LAST_NAME_RE.match(name)

# Checks to see if a given password is valid
USER_PW = re.compile(r"^.{6,32}$")
def valid_password(password):
    return password and USER_PW.match(password)

USER_EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return email and USER_EMAIL.match(email)

# Returns a hashed string
def hashstr(s):
    return new(SECRET, s).hexdigest()

# Returns a string with tha hash in the form of "x|0123456789abcdef"
def make_secure(v):
    return "%s%s%s" % (v, SEP, hashstr(v))

# Given a hash, it returns the value of the cookie, if it is valid
# if not valid it returns None
def check_secure(h):
    val = h.split(SEP)[0]
    if make_secure(val) == h:
        return val

def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime(__dateformat__)

def normalize(string):
    return string.lower()
