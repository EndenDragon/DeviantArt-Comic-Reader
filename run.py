#!/usr/bin/env python2
from comicreader.app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
