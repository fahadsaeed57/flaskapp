from flask import Flask
from flask import request
from flask import make_response , jsonify
import json
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
# initialize the flask app
app = Flask(__name__)
def formatlinks(data):
    links = data.get("links")
    links = links[1:len(links)-1]
    linksspliting = links.split("'")
    output = "The links we found use ful are \n"
    newlinks = []
    for link in linksspliting:
        if "http" in link:
            newlinks.append(link)
    for newlink in newlinks:
        output = output + newlink + "\n"
    return { "speech" : output} 
def processRequest(req):
    # if req.get("result").get("action") != "web.search":
    #     return {
    #         "speech" : "action not handled from webhook"
    #     }
    result = req.get("result")
    parameters = result.get("parameters")
    number = parameters['number']
    query = {"query" : parameters['q']}
    q = urlencode(query)
    
    if number and int(number) > 0 and int(number) <= 10:
        baseurl = "https://googlesearchapp.herokuapp.com/?"+q+"&limit="+str(number)
    # elif int(number) > 10 or int(number) < 0:
    #     return { "speech" : "Sorry more than 10 links are not allowed" }  
    elif not number:
        baseurl = "https://googlesearchapp.herokuapp.com/?"+q+"&limit=2"
    else:
        pass
    
    result = urlopen(baseurl).read()
    data = json.loads(result)
    res = formatlinks(data)
    return res
@app.route('/webhook', methods=['POST'])
def static_reply():
    req = request.get_json(silent=True, force=True) 
    responses = processRequest(req)
    res = json.dumps(responses, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# run the app
if __name__ == '__main__':
   app.run(debug=True) 


