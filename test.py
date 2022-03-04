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

sentOTP(apik,9774546207,sendern,"Your OTP is "+str(129934))