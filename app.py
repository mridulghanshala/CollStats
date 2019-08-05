from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, \
    send_from_directory, session
import Searching, Parse
import datetime
import time

app = Flask(__name__, static_url_path='/static')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_complete(path):
    typeVal = request.args.get('type', None)
    if typeVal != None:
        if typeVal.lower() == 'all':
            typeVal = None
    if len(path) < 5:
        return path + " is an invalid school name"
    thread = "https://talk.collegeconfidential.com/" + path
    database, countVal = Searching.search_all(thread, typeVal)
    for keyName in database.keys():
        for i, val in enumerate(database[keyName]):
            database[keyName][i] = Parse.parse_html(val)
    database2 = []
    order = ["accepted", "rejected", "unknown"]
    totalCount = 0
    for k in order:
        info = {}
        info["decision"] = k
        info["results"] = sorted(database[k],
                                 key=lambda e: datetime.datetime(*time.strptime(e['dtString'], "%Y-%m-%d")[:6]),
                                 reverse=True)
        totalCount += len(info['results'])
        database2.append(info)
    if typeVal == None:
        typeVal = ""
    else:
        typeVal += " "
    schoolName = path.split("?")[0].replace("-", " ").title()
    return render_template('results.html', schoolName=schoolName, typeVal=typeVal.title(), database=database2,
                           choices=[database.keys()], resultCount=totalCount)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    thread = request.form['projectFilepath']
    database, countVal = Searching.search_all(thread)

    for keyName in database.keys():
        for i, val in enumerate(database[keyName]):
            database[keyName][i] = Parse.parse_html(val)
    database2 = []
    order = ["accepted", "rejected", "unknown"]
    for k in order:
        info = {}
        info["decision"] = k
        info["results"] = sorted(database[k],
                                 key=lambda e: datetime.datetime(*time.strptime(e['dtString'], "%Y-%m-%d")[:6]),
                                 reverse=True)
        database2.append(info)
    return render_template('results.html', database=database2, choices=[database.keys()])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
