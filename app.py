from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)


data0= pd.read_csv('https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv')
cols1=data0.columns.tolist()
data1=data0.copy()
for i in range(1,len(cols1)):
    item=cols1[i]
    data1[item]=data0[item].rolling(window=7).mean()
data2=data1.copy()
for i in range(7,len(data2)):
    for j in range(1,len(cols1)):
        data2.iloc[i,j]=(data1.iloc[i,j]-data1.iloc[i-7,j])/7
data3=data2[-28:]
data3=data3.drop('ALL',axis=1)
date0=data3.iloc[-1,0]
data4=data3[-1:].T[1:]
data4.columns=['weekly mean increase']
data4=data4.sort_values('weekly mean increase',ascending=False)
data4['prefecture']=data4.index.tolist()
fig = px.bar(data4, x='prefecture', y='weekly mean increase',title="The latest ranknig of weekly mean increase ("+date0+")")
graph_html = fig.to_html(full_html=False)


@app.route('/')
def index():
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)



