from flask import Flask, render_template, request
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg');

app = Flask(__name__)

excle_data = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global excle_data
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file is selected')
    if file:
        excle_data = pd.read_excel(file)
        return render_template('analyse.html')

    return render_template('index.html', message='File not uploaded')

@app.route('/view_data')
def analysis():
    global excle_data
    if excle_data is not None:
        return render_template('view_data.html', data=excle_data.to_html())
    else:
        return render_template('view_data.html',error='No data to analyze')

@app.route('/graph', methods=['GET', 'POST'])
def graph_visual():
    global excle_data
    if request.method=='POST':
        x_axis=request.form['x-axis']
        y_axis=request.form['y-axis']
        
        plt.plot(excle_data[x_axis],excle_data[y_axis])
        plt.xlabel(x_axis)  # Corrected label
        plt.ylabel(y_axis)  # Corrected label
        plt.title('Plot from Excel Data')

        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()  # Close the plot to avoid memory leaks
        image_stream.seek(0)

        # Encode plot image to base64
        encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
        return render_template('graph_plot.html', plot_url=encoded_image)
    
    return render_template('graph_plot.html')

if __name__ == '__main__':
    app.run(debug=True)
