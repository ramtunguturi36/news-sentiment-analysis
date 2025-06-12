from http.server import BaseHTTPRequestHandler
from app import app
import json

def handler(event, context):
    # This function will be called by Vercel
    with app.test_request_context(path=event['path'], method=event['httpMethod'], headers=event['headers'], data=event.get('body', '')):
        response = app.full_dispatch_request()
    
    return {
        'statusCode': response.status_code,
        'body': response.get_data(as_text=True),
        'headers': dict(response.headers)
    }
