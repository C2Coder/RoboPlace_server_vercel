#!/bin/python3

from flask import Flask, request
from flask_cors import CORS
import pickle
from threading import Thread
import time
import os

import psycopg2

conn = psycopg2.connect(database=os.environ.get("POSTGRES_DATABASE"),
                        host=os.environ.get("POSTGRES_HOST"),
                        user=os.environ.get("POSTGRES_USER"),
                        password=os.environ.get("POSTGRES_PASSWORD"),
                        port=5432)


pixels = [[0 for i in range(100)] for j in range(100)]

chars = ["a", "b", "c", "d", "e", "f", "g", "h",
         "i", "j", "k", "l", "m", "n", "o", "p",]

colors = ['white', 'platinum', 'grey', 'black', 'pink', 'red', 'orange',
          'brown', 'yellow', 'lime', 'green', 'cyan', 'lblue', 'blue', 'mauve', 'purple']

hex_colors = ['#FFFFFF', '#E4E4E4', '#888888', '#222222', '#FFA7D1', '#E50000', '#E59500',
              '#A06A42', '#E5D900', '#94E044', '#02BE01', '#00D3DD', '#0083C7', '#0000EA', '#CF6EE4', '#820080']

cur = conn.cursor()
cur.execute("SELECT color FROM pixels ORDER BY id")
colors = cur.fetchall()
for y in range(100):
    for x in range(100):
        pixels[x][y] = chars.index(colors[(y*100)+x][0])
#print(pixels)


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
            # if data[0] == 'fill':
            #     print("filling")
            #     for y in range(100):
            #         for x in range(100):
            #             pixels[x][y] = int(colors.index(data[1].replace(" ", "")))
            # else:
            #     pixels[int(data[0])][int(data[1])] = int(colors.index(data[2].replace(" ", "")))
            #     print(pixels[int(data[0])][int(data[1])])


            # how these lines feel -> https://discord.com/assets/633e893d2577bb3de002991aa00bc3b0.svg

            #return str(pixels[int(data[0])][int(data[1])]) + ", " + data[2] 
            return colors.index(data[2])
            pixels[int(data[0])][int(data[1])] = int(colors.index(data[2]))
            try:
                cur.execute("UPDATE pixels SET color = " + colors[pixels[x][y]]+ " WHERE id = " + str((y*100)+x))
                conn.commit()
            except Exception:
                return "sql failed"
            return "gut"
        except:
            print("failed")
            return 'failed'



if __name__ == '__main__':
    app.run()