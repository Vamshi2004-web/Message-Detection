from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import pandas as pd
import xgboost as xgb
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
import os
import pickle

# HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>URL Detection</title>
  <style>
    body {{
      background: linear-gradient(to bottom, #00c6ff 0%, #0072ff 100%);
      font-family: Arial, sans-serif;
      text-align: center;
      margin-top: 100px;
      color: white;
    }}
    input[type="text"] {{
      padding: 10px;
      width: 300px;
      border-radius: 5px;
      border: none;
      margin-bottom: 20px;
    }}
    button {{
      padding: 10px 20px;
      background-color: #28a745;
      border: none;
      color: white;
      font-size: 16px;
      border-radius: 5px;
      cursor: pointer;
    }}
    .result {{
      margin-top: 20px;
      background: white;
      color: black;
      padding: 15px;
      border-radius: 10px;
      display: inline-block;
      font-size: 20px;
    }}
  </style>
</head>
<body>
  <h1>URL Detection</h1>
  <form method="POST" action="/">
    <input type="text" name="url" placeholder="Enter URL here" required><br>
    <button type="submit">Check URL</button>
  </form>
  <div class="result">
    {result}
  </div>
</body>
</html>
"""

# Feature engineering function
def feature_engineering(url):
    features = []
    features.append(len(url))
    features.append(url.count('@'))
    features.append(url.count('www'))
    features.append(url.count('https'))
    features.append(url.count('.'))
    features.append(url.count('/'))
    features.append(url.count('='))
    features.append(url.count('-'))
    features.append(url.count('?'))
    features.append(url.count('%'))
    features.append(url.count('_'))
    features.append(url.count('&'))
    features.append(url.count(' '))
    return features

# Model loading or training
def load_models():
    if os.path.exists('xgb_model.pkl') and os.path.exists('lgb_model.pkl'):
        xgb_model = pickle.load(open('xgb_model.pkl', 'rb'))
        lgb_model = pickle.load(open('lgb_model.pkl', 'rb'))
    else:
        df = pd.read_csv('malicious_phish1.csv', encoding='ISO-8859-1')
        X = [feature_engineering(url) for url in df['url']]
        X = pd.DataFrame(X)
        y = pd.get_dummies(df['type'])
        y_labels = y.values.argmax(axis=1)

        X_train, _, y_train, _ = train_test_split(X, y_labels, test_size=0.2, random_state=42)

        xgb_model = xgb.XGBClassifier()
        xgb_model.fit(X_train, y_train)
        pickle.dump(xgb_model, open('xgb_model.pkl', 'wb'))

        lgb_model = LGBMClassifier()
        lgb_model.fit(X_train, y_train)
        pickle.dump(lgb_model, open('lgb_model.pkl', 'wb'))
    return xgb_model, lgb_model

# Load models once
xgb_model, lgb_model = load_models()

# Request handler
class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_template.format(result="").encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_qs(post_data)
        url = form_data.get('url', [''])[0]

        safe_urls = ['youtube.com', 'google.com', 'wikipedia.org', 'amazon.com', 'facebook.com', 'whatsapp.com', 'chatgpt.com' ]

        if any(safe_url in url for safe_url in safe_urls):
            result = "Not Spam "
        else:
            features = feature_engineering(url)
            xgb_pred = xgb_model.predict([features])[0]
            lgb_pred = lgb_model.predict([features])[0]

            if xgb_pred == 0 and lgb_pred == 0:
                result = "Not Spam"
            else:
                result = "Spam"

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = html_template.format(result=result)
        self.wfile.write(response.encode('utf-8'))

if __name__ == "__main__":
    port = 8086
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()