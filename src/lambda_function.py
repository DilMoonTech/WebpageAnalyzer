import json
from urllib.parse import urlparse
from analyzer import WebpageAnalyzer

headers =  {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }

def lambda_handler(event, context):
    """
    Lambda handler for webpage analysis
    Expected event format:
    {
        "url": "https://example.com"
    }
    """
    try:
        print("Event:", json.dumps(event))  # This will appear in CloudWatch logs
        # Get URL from event
        # Get query parameters
        query_parameters = event.get('queryStringParameters', {})
        path_parameters = event.get('pathParameters', {})

        print("Query parameters:", query_parameters)  # Debug logging
        print("Path parameters:", path_parameters)    # Debug logging

        #url = event.get('url')
        if not query_parameters or 'url' not in query_parameters:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': 'URL is required',
                    'usage': 'Add ?url=https://example.com to your request',
                    'received_event': {
                        'path': event.get('path'),
                        'queryStringParameters': query_parameters,
                        'pathParameters': path_parameters
                    }
                })
            }
        
        url = query_parameters['url']
        req_headers = event.get('headers', {})

        # Extract domain from URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

         # Filter and construct headers
        filtered_headers = {
            'User-Agent': req_headers.get('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'Accept': req_headers.get('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9'),
            'Accept-Language': req_headers.get('Accept-Language', 'en-US,en;q=0.5'),
            'Host': domain  # Set host header to the domain from URL
        }

        print("Filtered headers:", filtered_headers)  # Debug logging

        # Create analyzer and get results
        analyzer = WebpageAnalyzer(url, filtered_headers)
        analysis_results = analyzer.analyze()

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(analysis_results)
        }

    except Exception as e:
        print("Error:", str(e))  # This will appear in CloudWatch logs
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': str(e),
                #'event': event  # Include event for debugging
            })
        }
