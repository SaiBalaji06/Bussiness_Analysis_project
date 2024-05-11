from flask import *
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pdfkit

app = Flask(__name__)

# Sample data (replace this with your actual data)
data = "C:\\Users\\saibalaji\\Downloads\\DA+Workshop+Dataset.xlsx"

df = pd.read_excel(data)
def generate_graph_chart():
    plt.plot(df['Date'],df['Total sales'])
    plt.show()
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()  # Close the plot to avoid memory leaks
    image_stream.seek(0)

    # Encode plot image to base64
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
    return encoded_image

# Function to generate pie chart and convert to base64 for embedding
def generate_pie_chart():
    category_counts = df['Category'].value_counts()
    # Use Agg backend explicitly
    plt.switch_backend('Agg')

    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Category Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Save plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()  # Close the plot to avoid memory leaks
    image_stream.seek(0)

    # Encode plot image to base64
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    return encoded_image

@app.route('/')
def index():
    # Generate the pie chart and pass the base64-encoded image to the template
    pie_chart_image = generate_pie_chart()
    graph_chart_image = generate_graph_chart()
    return render_template('index.html', pie_chart_image=pie_chart_image, graph_chart_image=graph_chart_image)

def generate():
    pie_chart_image = generate_pie_chart()
    return render_template('htpcon.html', pie_chart_image=pie_chart_image)

def read_html_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()

@app.route('/generate_pdf')
def generate_pdf():
    # Generate the pie chart
    pie_chart_image = generate_pie_chart()

    #reading the HTML content and replacing the visual images
    html_template = read_html_template('C:\\Users\\saibalaji\\Desktop\\php\\templates\\htpcon.html')
    html_content = html_template.replace('{{ pie_chart_image }}', pie_chart_image)
    
    path_to_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options={'image-dpi': 300, 'enable-local-file-access': None})

    return send_file(BytesIO(pdf_data), as_attachment=True, download_name='samplehtmltopdf.pdf')

if __name__ == '__main__':
    app.run(debug=True)
