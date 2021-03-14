import flask
from getinfo import getInfo


app = flask.Flask(__name__)
app.config["DEBUG"] = True

curr = getInfo("czk")


@app.route('/', methods=['GET'])
def home():
    return "<h1>czc.cz/alza web scrapper api</h1><p>This site is a prototype API for www.czc.cz/www.alza.cz web scraper</p>"


@app.route('/czc/<name>/<identifier>/<currency>', methods=['GET'])
def czc_api(name, identifier, currency):
    if name.startswith("https://www.czc.cz/"):
        return {"error": "you passed the whole url please pass only the name and id like this name/"}
    if currency not in curr.available_currencies:
        return {"error": f"currency passed to this class isnt in our list of currencies please use any of these {curr.available_currencies} if you don't use any of these currencies this will cause error"}
    else:
        gi = getInfo(currency)
        return gi.get_info("https://www.czc.cz/"+name+"/"+identifier+"/produkt")

@app.route('/alza/<name>/<currency>', methods=['GET'])
def alza_api(name, currency):
    if name.startswith("https://www.czc.cz/"):
        return {"error": "you passed the whole url please pass only the name and id like this name/"}
    if currency not in curr.available_currencies:
        return {"error": f"currency passed to this class isnt in our list of currencies please use any of these {curr.available_currencies} if you don't use any of these currencies this will cause error"}
    else:
        gi = getInfo(currency)
        return gi.get_info("https://www.alza.cz/"+name+".htm")


app.run()
