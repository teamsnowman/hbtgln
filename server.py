from flask import Flask, request, jsonify, render_template
import random
import datetime

app = Flask(__name__, static_url_path='')

if __name__ == '__main__':
    app.debug = True
    app.run(threaded = True)

   