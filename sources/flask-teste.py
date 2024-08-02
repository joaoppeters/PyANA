from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'sua_senha':
            return render_template('graph.html')  # Página com o gráfico
        else:
            return redirect(url_for('index'))
    return 

if __name__ == '__main__':
    app.run(debug=True)
