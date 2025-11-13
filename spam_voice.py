
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import pandas as pd

# HTML template with voice input and enhanced result presentation
html_template = """ 
<!DOCTYPE html> 
<html> 
<head> 
  <meta charset="UTF-8"> 
  <title>Voice Detection System</title> 
  <style> 
    body {{ 
      text-align: center; 
      margin-top: 200px; 
      font-family: Arial, sans-serif; 
    }} 
    .login {{ 
      text-align: center; 
      background-color: rgba(255, 255, 255, 0.8); 
      padding: 20px; 
      border-radius: 10px; 
      display: inline-block; 
    }} 
    textarea {{ 
      border: 2px solid #333; 
      border-radius: 5px; 
      padding: 10px; 
      font-family: Arial, sans-serif; 
      font-size: 16px; 
      background-color: #f9f9f9; 
      color: #333; 
      width: 90%; 
      max-width: 500px; 
      margin-top: 10px; 
      resize: none; 
    }} 
    textarea[readonly] {{ 
      background-color: #e9e9e9; 
    }} 
    button {{ 
      background-color: #04AA6D; 
      border: none; 
      color: white; 
      padding: 15px 32px; 
      text-align: center; 
      text-decoration: none; 
      display: inline-block; 
      font-size: 16px; 
      margin: 10px; 
      border-radius: 5px; 
    }} 
    .results {{ 
      margin-top: 20px; 
    }} 
    .result-box {{ 
  background-color: #ffffff; 
  border: 2px solid #333; 
  border-radius: 5px; 
  padding: 20px; 
  display: inline-block; 
  font-size: 18px; 
  color: #333; 
  max-width: 90%; /* Increase this value to make the box wider */ 
  margin-top: 10px; /* Optionally adjust the top margin */ 
}} 
  </style> 
</head> 
<body> 
  <div class="login"> 
    <h1>Voice Detector</h1> 
    <form action="/" method="post" id="spamForm"> 
      <textarea name="message" id="message" rows="6" cols="50" readonly>{message}</textarea> 
      <br> 
      <button type="button" onclick="startRecognition()">Start Voice Input</button> 
      <button type="submit">Predict</button> 
      <button type="button" onclick="window.location='http://localhost:8084/spamdetection_2/dashboard.html'" style="background-color: #f44336; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;"> 
        Back 
      </button> 
      <div class="results"> 
        {result} 
      </div> 
    </form> 
  </div> 
  <script> 
    function startRecognition() {{ 
      var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)(); 
      recognition.lang = 'en-US'; 
      recognition.interimResults = false; 
      recognition.maxAlternatives = 1; 

      recognition.start(); 

      recognition.onresult = function(event) {{ 
        var transcript = event.results[0][0].transcript; 
        document.getElementById('message').value = transcript; 
      }}; 

      recognition.onerror = function(event) {{ 
        console.error('Speech recognition error', event); 
      }}; 
    }} 
  </script> 
</body> 
</html> 
"""


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_template.format(message='', result='').encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_qs(post_data)
        message = form_data.get('message', [''])[0]

        df = pd.read_csv("spam.csv", encoding="latin-1")
        df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
        df['label'] = df['class'].map({'ham': 0, 'spam': 1})
        X = df['message']
        y = df['label']
        cv = CountVectorizer()
        X = cv.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        clf = MultinomialNB()
        clf.fit(X_train, y_train)
        clf.score(X_test, y_test)

        vect = cv.transform([message]).toarray()
        prediction = clf.predict(vect)[0]
        confidence = clf.predict_proba(vect)[0][1]

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        result = "Spam" if prediction == 1 and confidence >= 0.99910 else "Not Spam"
        response = html_template.format(message=message,
                                        result=f'<div class="result-box"><p>Prediction: {result}</p></div>')
        self.wfile.write(response.encode('utf-8'))


if __name__ == '__main__':
    port = 8087
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()