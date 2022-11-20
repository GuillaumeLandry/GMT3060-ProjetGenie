# https://www.geeksforgeeks.org/how-to-build-a-simple-android-app-with-flask-backend/

from flask import Flask, request, render_template
import json
 
app = Flask(__name__)

data_packets = []
 
@app.route("/")
def show_home():
    return render_template('index.html', packets=data_packets)

@app.route('/viz')
def show_viz():
   return render_template('threejs-template.html')

@app.route("/debug", methods=["POST"])
def show_debug():
    new_data = request.form["sample"]
    print("Received : " + new_data)

    data_packets.append(new_data)
    with open('./data/data_packets.txt', 'w') as fp:
        for packet in data_packets:
            # write each item on a new line
            fp.write("%s\n" % packet)
    with open('./data/data_packets.json', 'w') as fp:
        json.dump(data_packets, fp, indent=4)
        fp.write()

    render_template('index.html', packets=data_packets)
    return "received"

if __name__ == "__main__":
    app.run(host="0.0.0.0")