from flask import Flask, Response
from flask_cors import CORS
import pandas as pd
import json
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/crimeLocs', methods = ['GET','POST'])
def crimeLocs():
    # df = pd.read_csv('crime_data.csv')
    # location_list = []
    # n = len(df['Location'])
    # for i in range(n):
    #     location_list.append(df['Location'][i])
    # dic = {'result': location_list}
    with open('crime_points_2020.json','rb') as f:    
        return  Response(f.read(), status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run()
