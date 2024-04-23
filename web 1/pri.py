from flask import Flask, render_template, request, send_file
import boto3

app = Flask(__name__)

# AWS credentials
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
S3_BUCKET_NAME = ''

# Initialize S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Collect user details
        name = request.form['name']
        email = request.form['email']
        # Format data into text file
        data = f"Name: {name}\nEmail: {email}"
        # Write data to text file
        with open('user_details.txt', 'w') as file:
            file.write(data)
        # Upload text file to S3 bucket
        s3.upload_file('user_details.txt', S3_BUCKET_NAME, 'user_details.txt')
        return render_template('success.html')

@app.route('/download')
def download():
    # Fetch file from S3 bucket
    s3.download_file(S3_BUCKET_NAME, 'user_details.txt', 'user_details.txt')
    # Return file for download
    return send_file('user_details.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
