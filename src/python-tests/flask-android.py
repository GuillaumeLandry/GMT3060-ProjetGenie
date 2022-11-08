# https://www.geeksforgeeks.org/how-to-build-a-simple-android-app-with-flask-backend/

from flask import Flask, request
 
# Flask Constructor
app = Flask(__name__)
 
# decorator to associate
# a function with the url
@app.route("/")
def showHomePage():
      # response from the server
    return "This is home page"

@app.route("/debug", methods=["POST"])
def debug():
    text = request.form["sample"]
    print(text)
    return "received"

if __name__ == "__main__":
  app.run(host="0.0.0.0")