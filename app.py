import os
from flask import Flask, render_template, request, redirect, send_file, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

import subprocess
import shlex
from flask import make_response

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

    # Check if mode is '-x'
    if mode == '-x':
        # Read the content of output.txt
        with open('output.txt', 'r') as file:
            output_text = file.read()

        # Create a response with the output text
        response = make_response(output_text)
        # Set the Content-Disposition header to inline
        response.headers['Content-Disposition'] = 'inline'

        return response

    # Redirect to the preview page for other modes
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
