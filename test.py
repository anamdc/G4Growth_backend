import urllib
import urllib.parse
import urllib.request

apik="NTM3MzY2NTI1OTc1NzM1ODM4NmU3NTMwNDEzMTZjNTg="
sendern="BOOKRO"


def sentOTP(apikey,numbers,sender,message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    print(fr)
    return True
template = f"Your Login OTP for Bookkaaro is {123456}. Please do not share this with anyone."
sentOTP(apik,9774546207,sendern,template)