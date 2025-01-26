import pytest
import responses
from src.analyzer import WebpageAnalyzer
from pathlib import Path

test_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Host": "example.com",
}


@pytest.fixture
def sample_html():
    fixture_path = Path(__file__).parent / "fixtures" / "sample_webpage.html"
    return fixture_path.read_text()


@pytest.fixture
def analyzer():
    return WebpageAnalyzer("https://example.com", test_header)


class TestWebpageAnalyzer:
    @responses.activate
    def test_fetch_page(self, analyzer, sample_html):
        # Setup mock
        responses.add(
            responses.GET,
            "https://example.com",
            body=sample_html,
            status=200,
            content_type="text/html",
        )

        analyzer.fetch_page()
        assert analyzer.soup is not None

    @responses.activate
    def test_analyze_returns_complete_structure(self, analyzer, sample_html):
        # Setup mock
        responses.add(
            responses.GET,
            "https://example.com",
            body=sample_html,
            status=200,
            content_type="text/html",
        )

        results = analyzer.analyze()

        assert isinstance(results, dict)
        assert all(
            key in results
            for key in [
                "tag_count",
                "meta_info",
                "links_analysis",
                "heading_structure",
                "images",
                "text_stats",
            ]
        )

    @responses.activate
    def test_count_tags(self, analyzer, sample_html):
        # Setup mock
        responses.add(
            responses.GET,
            "https://example.com",
            body=sample_html,
            status=200,
            content_type="text/html",
        )

        analyzer.fetch_page()
        tag_count = analyzer._count_tags()

        assert tag_count["h1"] == 1
        assert tag_count["h2"] == 1
        assert tag_count["a"] == 2
        assert tag_count["img"] == 2

    @responses.activate
    def test_analyze_meta(self, analyzer, sample_html):
        # Setup mock
        responses.add(
            responses.GET,
            "https://example.com",
            body=sample_html,
            status=200,
            content_type="text/html",
        )

        analyzer.fetch_page()
        meta_info = analyzer._analyze_meta()

        assert meta_info["description"] == "Test webpage"

    @responses.activate
    def test_analyze_links(self, analyzer, sample_html):
        # Setup mock
        responses.add(
            responses.GET,
            "https://example.com",
            body=sample_html,
            status=200,
            content_type="text/html",
        )

        analyzer.fetch_page()
        links_analysis = analyzer._analyze_links()

        assert links_analysis["total_links"] == 2
        assert links_analysis["external_links_count"] == 1
        assert links_analysis["internal_links_count"] == 1

    @responses.activate
    def test_analyze_images(self, analyzer, sample_html):
        # Setup mock
        responses.add(
            responses.GET,
            "https://example.com",
            body=sample_html,
            status=200,
            content_type="text/html",
        )

        analyzer.fetch_page()
        images_analysis = analyzer._analyze_images()

        assert images_analysis["total_images"] == 2
        assert images_analysis["images_with_alt"] == 1

    @responses.activate
    def test_fetch_page_error_handling(self, analyzer):
        # Setup mock
        responses.add(responses.GET, "https://example.com", status=404)

        with pytest.raises(Exception) as exc_info:
            analyzer.fetch_page()
        assert "Failed to fetch webpage" in str(exc_info.value)
