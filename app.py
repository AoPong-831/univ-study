from flask import Flask,render_template, request, redirect, Response, make_response
app = Flask(__name__)



@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "POST":
        name = request.form["entry"]

        print("="*100)
        print(name)
        return redirect("/")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)