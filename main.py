from flask import Flask, request, jsonify, send_from_directory
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(app.static_folder, path)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        visualization_type = request.form.get('visualizationType')
        
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400
        if not visualization_type:
            return jsonify({'error': 'Visualization type not specified'}), 400
        
        data = file.read().decode('utf-8')
        plot = create_plot(visualization_type, data)
        return jsonify({'plot': plot, 'success': True}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_plot(visualization_type, data):
    try:
        df = pd.read_csv(io.StringIO(data))
        plt.figure(figsize=(9.4,4))
        
        if visualization_type == 'scatter':
            create_scatter_plot(df)
        elif visualization_type == 'radar':
            create_radar_chart(df)
        elif visualization_type == 'hexbin':
            create_hexbin_plot(df)
        elif visualization_type == 'line':
            create_line_plot(df)
        else:
            return jsonify({'error': 'Invalid visualization type'}), 400
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        return plot
    
    except Exception as e:
        return str(e)

def create_scatter_plot(df):
    x_column, y_column = df.columns[:2]
    plt.scatter(df[x_column], df[y_column], color='blue', alpha=0.5)
    plt.title('Scatter Plot')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid(True)




def create_hexbin_plot(df):
    x_column, y_column = df.columns[:2]
    plt.hexbin(df[x_column], df[y_column], gridsize=20, cmap='Blues')
    plt.colorbar(label='count in bin')
    plt.title('Hexbin Plot')
    plt.xlabel(x_column)
    plt.ylabel(y_column)

def create_line_plot(df):
    x_column, y_column = df.columns[:2]
    plt.plot(df[x_column], df[y_column], marker='o', color='blue', linestyle='-')
    plt.title('Line Plot')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid(True)

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg')
    app.run(debug=True, threaded=False)
