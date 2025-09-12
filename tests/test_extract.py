import requests
import datetime
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from utils.extract import fetching_content, extract_fashion_data, scrape_fashion


# ---------- Test fetching_content ----------
@patch("utils.extract.requests.Session.get")
def test_fetching_content_success(mock_get):
    mock_response = MagicMock()
    mock_response.content = b"<html>OK</html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    content = fetching_content("http://example.com")
    assert content == b"<html>OK</html>"


@patch("utils.extract.requests.Session.get")
def test_fetching_content_failure(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    content = fetching_content("http://example.com")
    assert content is None


# ---------- Test extract_fashion_data ----------
def test_extract_fashion_data_with_price_container():
    html = """
    <div class="product-details">
        <h3>Sample Product</h3>
        <div class="price-container"><span class="price">$100</span></div>
        <p>4.5 Stars</p>
        <p>Red, Blue</p>
        <p>L</p>
        <p>Men</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    product_details = soup.find("div", class_="product-details")

    result = extract_fashion_data(product_details)
    assert result["Title"] == "Sample Product"
    assert result["Price"] == "$100"
    assert result["Rating"] == "4.5 Stars"
    assert result["Colors"] == "Red, Blue"
    assert result["Size"] == "L"
    assert result["Gender"] == "Men"
    assert isinstance(result["Timestamp"], datetime.datetime)


def test_extract_fashion_data_without_price_container():
    html = """
    <div class="product-details">
        <h3>Another Product</h3>
        <p>$200</p>
        <p>3.5 Stars</p>
        <p>Black</p>
        <p>M</p>
        <p>Women</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    product_details = soup.find("div", class_="product-details")

    result = extract_fashion_data(product_details)
    assert result["Title"] == "Another Product"
    assert result["Price"] == "$200"
    assert result["Rating"] == "3.5 Stars"
    assert result["Colors"] == "Black"
    assert result["Size"] == "M"
    assert result["Gender"] == "Women"


def test_extract_fashion_data_error():
    result = extract_fashion_data(None)  # passing invalid element
    assert result is None


# ---------- Test scrape_fashion ----------
@patch("utils.extract.fetching_content")
def test_scrape_fashion_single_page(mock_fetch):
    html = """
    <html>
    <body>
        <div class="product-details">
            <h3>Single Product</h3>
            <p>$50</p>
            <p>5 Stars</p>
            <p>Green</p>
            <p>S</p>
            <p>Unisex</p>
        </div>
    </body>
    </html>
    """
    # first call has content, second call is None so the loop stops
    mock_fetch.side_effect = [html.encode("utf-8"), None]

    result = scrape_fashion("http://example.com", start_page=2, delay=0)
    assert len(result) == 1
    assert result[0]["Title"] == "Single Product"


@patch("utils.extract.fetching_content")
def test_scrape_fashion_with_next_page(mock_fetch):
    first_page_html = """
    <html>
    <body>
        <div class="product-details">
            <h3>First Product</h3>
            <p>$10</p>
            <p>4 Stars</p>
            <p>Blue</p>
            <p>M</p>
            <p>Men</p>
        </div>
        <li class="page-item next"></li>
    </body>
    </html>
    """
    second_page_html = """
    <html>
    <body>
        <div class="product-details">
            <h3>Second Product</h3>
            <p>$20</p>
            <p>5 Stars</p>
            <p>Red</p>
            <p>L</p>
            <p>Women</p>
        </div>
    </body>
    </html>
    """

    # mock return values for each call
    mock_fetch.side_effect = [
        first_page_html.encode("utf-8"),
        second_page_html.encode("utf-8"),
        None,  # stop scraping
    ]

    result = scrape_fashion("http://example.com", start_page=2, delay=0)
    assert len(result) == 2
    assert result[0]["Title"] == "First Product"
    assert result[1]["Title"] == "Second Product"
