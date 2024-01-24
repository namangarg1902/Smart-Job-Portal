from flask import Flask, render_template, jsonify , request
from main.main import fetch_shine , fetch_times  # Replace 'your_module' and 'your_function' with your actual module and function names

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    jsonData1 = None
    jsonData2 = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        jsonData1 = fetch_shine(user_input)
        jsonData2 =fetch_times(user_input)
        
    return render_template('index.html' , jsonData1 = jsonData1 , jsonData2 = jsonData2)
    

    # return render_template('index.html', jsonData=(jsonData))


    # Call your Python function that returns JSON data
    # json_data = lambda_handler("Developer")
    # print(json_data)
    # return render_template('index.html', jsonData=(json_data))

    # return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)
