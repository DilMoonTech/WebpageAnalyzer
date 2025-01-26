import json
import pytest
from src.lambda_function import lambda_handler
from unittest.mock import patch

@pytest.fixture
def valid_event():
    return {
        "httpMethod": "GET",
        "queryStringParameters": {
            "url": "https://example.com"
        },
    }

@pytest.fixture
def analysis_result():
    return {
        "tag_count": {"div": 1, "p": 1},
        "meta_info": {"description": "Test"},
        "links_analysis": {
            "total_links": 2,
            "internal_links_count": 1,
            "external_links_count": 1
        },
        "heading_structure": {"h1": 1},
        "images": {
            "total_images": 2,
            "images_with_alt": 1
        },
        "text_stats": {
            "word_count": 10,
            "character_count": 50
        }
    }

class TestLambdaHandler:
    def test_missing_url(self):
        response = lambda_handler({}, None)
        assert response['statusCode'] == 400
        assert 'URL is required' in response['body']

    @patch('analyzer.WebpageAnalyzer.analyze')
    def test_successful_analysis(self, mock_analyze, valid_event, analysis_result):
        mock_analyze.return_value = analysis_result
        
        response = lambda_handler(valid_event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert all(key in body for key in analysis_result.keys())

    @patch('analyzer.WebpageAnalyzer.analyze')
    def test_analyzer_error(self, mock_analyze, valid_event):
        mock_analyze.side_effect = Exception("Analysis failed")
        
        response = lambda_handler(valid_event, None)
        
        assert response['statusCode'] == 500
        assert 'Analysis failed' in response['body']
