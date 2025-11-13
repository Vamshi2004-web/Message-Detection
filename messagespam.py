from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import pandas as pd

# HTML template without the <script> block
html_template = """ 
<!DOCTYPE html> 
<html> 
<head> 
  <meta charset="UTF-8"> 
  <title>Message Detection System</title> 
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
      resize: vertical; 
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
      cursor: pointer; 
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
      max-width: 90%; 
      margin-top: 10px; 
    }} 
  </style> 
</head> 
<body> 
  <div class="login"> 
    <h1>Message Detector</h1> 
    <form action="/" method="post"> 
      <!-- Removed readonly to allow typing -->
      <textarea name="message" id="message" rows="6" cols="50" required>{message}</textarea> 
      <br> 
      <button type="submit">Predict</button> 
      <button type="button" onclick="window.location='http://localhost:8084/spamdetection_2/dashboard.html'" style="background-color: #f44336;">Back</button> 
      <div class="results">{result}</div> 
    </form> 
  </div> 
</body> 
</html> 
"""

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(html_template.format(message='', result='').encode('utf-8'))

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length).decode('utf-8')
        message = parse_qs(post_data).get('message', [''])[0]

        # Load & preprocess dataset
        df = pd.read_csv("spam.csv", encoding="latin-1")
        df.drop(['Unnamed: 2','Unnamed: 3','Unnamed: 4'], axis=1, inplace=True)
        df['label'] = df['class'].map({'ham':0,'spam':1})
        X, y = df['message'], df['label']

        # Train vectorizer and model
        cv = CountVectorizer()
        X_vec = cv.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.33, random_state=42)
        clf = MultinomialNB().fit(X_train, y_train)

        # Predict
        vect = cv.transform([message]).toarray()
        pred = clf.predict(vect)[0]
        conf = clf.predict_proba(vect)[0][1]

        # Build result HTML
        result_html = (
          f'<div class="result-box">'
          f'<p>Entered Message: {message}</p>'
          f'<p>Prediction: {"Spam" if pred==1 else "Not Spam"}</p>'
          '</div>'
        )

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(html_template.format(message=message, result=result_html).encode('utf-8'))

if __name__ == '__main__':
    port = 8089
    print(f"Starting server on port {port}...")
    HTTPServer(('', port), MyRequestHandler).serve_forever()
