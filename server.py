from datetime import date
from flask import Flask, render_template, session, redirect,request
import random
app = Flask(__name__)

app.secret_key="Hello neighbor."

MAP= {
    "farm": (10,20),
    "cave": (5,10),
    "house": (2,5),
    "casino": (0, 50)
}
@app.route('/')
def index():
    if "gold" and "rounds" not in session:
        session["gold"]= 0
        session["results"]=[]
        session["rounds"]= 0
    return render_template("index.html")

@app.route('/process_money',methods=['POST'])
def process_gold():
    building_name= request.form['building']
    building = MAP[building_name]
    building_name_upper = building_name[0].upper() + building_name[1:]
    current_gold = random.randint(building[0], building[1])
    result= 'win'
    message= f'Earned {current_gold} from the {building_name}!'
    if building_name == 'casino':
        if random.randint(0,1) > 0:
            message = f"Entered a {building_name_upper} and lost {current_gold} golds..."
            current_gold = current_gold * -1
            result = 'lose'
    session["gold"] += current_gold
    session["rounds"] += 1
    session["results"].append({"message": message, "result":result})

    return redirect ('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')
    
if __name__=="__main__":
    app.run(debug=True)