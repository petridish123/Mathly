import os
from flask import Flask, render_template, request, redirect, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

import subprocess
import shlex

@app.route('/generate', methods=['POST'])
def generate():
    mode = request.form['flag']
    user_input = request.form['input']

    # Quote the user input to ensure it's treated as a single argument
    quoted_input = shlex.quote(user_input)

    # Build the command list with properly quoted arguments
    command = [r'C:\Users\julia\PycharmProjects\egacy23_24\Scripts\python.exe', 'main.py', mode, quoted_input]

    # Run the command using subprocess module for better control
    subprocess.run(command)

    # Redirect to the preview page
    return redirect('/preview')


@app.route('/preview')
def preview():
    # Get the directory where main.py is saved
    main_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(main_dir, 'output.pdf')

    if os.path.exists(pdf_path):
        return send_file(pdf_path)
    else:
        return "PDF file not found."

if __name__ == '__main__':
    app.run(debug=True)
