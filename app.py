from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import Searching,Parse
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
    database,countVal = Searching.search_all(thread, typeVal)
    for keyName in database.keys():
        for i, val in enumerate(database[keyName]):
            database[keyName][i] = Parse.parse_html(val)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
