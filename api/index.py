#!/bin/python3

from flask import Flask, request
from flask_cors import CORS
import pickle
from threading import Thread
import time
import os


pixels = [[0 for i in range(100)] for j in range(100)]

chars = ["a", "b", "c", "d", "e", "f", "g", "h",
         "i", "j", "k", "l", "m", "n", "o", "p",]


colors = ['white', 'platinum', 'grey', 'black', 'pink', 'red', 'orange',
          'brown', 'yellow', 'lime', 'green', 'cyan', 'lblue', 'blue', 'mauve', 'purple']

hex_colors = ['#FFFFFF', '#E4E4E4', '#888888', '#222222', '#FFA7D1', '#E50000', '#E59500',
              '#A06A42', '#E5D900', '#94E044', '#02BE01', '#00D3DD', '#0083C7', '#0000EA', '#CF6EE4', '#820080']

app = Flask(__name__)
CORS(app)

# main page

@app.route('/', methods=['GET'])
def main_page_response():
    with open("index.htm") as index_file:
        return index_file.read()


# request handlers

@app.route('/get_pixels', methods=['GET'])
def handle_request():
    if request.method == 'GET':
        #print(dict(args))
        response = ""
        for y in range(100):
            for x in range(100):
                response = response + str(chars[pixels[x][y]])
            response = response
        return response


@app.route('/post', methods=['POST'])
def handle_incoming():
    global pixels
    if request.method == 'POST':
        # Handle POST request
        try:
            data_in = str(request.get_json())
            #print(data_in)
            data_raw = data_in.replace("{", "").replace("}", "").replace("'", "").replace(":", "_")
            #print(data_raw)
            data = data_raw.split("_")
            print(data)
            if data[0] == 'fill':
                print("filling")
                for y in range(100):
                    for x in range(100):
                        pixels[x][y] = int(colors.index(data[1].replace(" ", "")))
            else:
                pixels[int(data[0])][int(data[1])] = int(colors.index(data[2].replace(" ", "")))
                print(pixels[int(data[0])][int(data[1])])
            #print('updated')  # yeah that works
            #print(pixels[int(data[0])][int(data[1])])
            return "gut"
        except:
            print("failed")
            return 'failed'



if __name__ == '__main__':
    app.run()