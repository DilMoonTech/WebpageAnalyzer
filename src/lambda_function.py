import json
from .analyzer import WebpageAnalyzer

def lambda_handler(event, context):
    """
    Lambda handler for webpage analysis
    Expected event format:
    {
        "url": "https://example.com"
    }
    """
    try:
        # Get URL from event
        url = event.get('url')
        if not url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'URL is required'})
            }

        # Create analyzer and get results
        analyzer = WebpageAnalyzer(url)
        analysis_results = analyzer.analyze()

        return {
            'statusCode': 200,
            'body': json.dumps(analysis_results)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
