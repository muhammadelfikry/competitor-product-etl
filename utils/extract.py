from bs4 import BeautifulSoup
import requests
import time
import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    """
    Fetch the HTML content of a given URL.

    This function sends a GET request with a predefined user-agent header
    to avoid being blocked by the website. If the request is successful, 
    the raw content is returned.

    Args:
        url (str): The target URL to fetch.

    Returns:
        bytes | None: The raw HTML content of the page if successful,
        otherwise None.
    """
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    try:
        response.raise_for_status()
        return response.content
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred when making requests to {url}: {e}")
        return None
    

def extract_fashion_data(product_details):
    """
    Extract fashion product data from a BeautifulSoup HTML element.

    This function parses the product details container and extracts key 
    attributes such as title, price, rating, available colors, size, 
    and gender. It also adds a timestamp when the data was extracted.

    Args:
        product_details (bs4.element.Tag): A BeautifulSoup element 
            containing product details.

    Returns:
        dict | None: A dictionary with extracted product information, or
        None if extraction fails.
    """
    try:
        title = product_details.find("h3").get_text(strip=True)
        price_container = product_details.find("div", class_="price-container")
        p_tags = product_details.find_all("p")

        if price_container:
            price = price_container.find("span", class_="price").get_text(strip=True)
            rating = p_tags[0].get_text(strip=True)
            colors = p_tags[1].get_text(strip=True)
            size = p_tags[2].get_text(strip=True)
            gender = p_tags[3].get_text(strip=True)
        
        else:
            price = p_tags[0].get_text(strip=True)
            rating = p_tags[1].get_text(strip=True)
            colors = p_tags[2].get_text(strip=True)
            size = p_tags[3].get_text(strip=True)
            gender = p_tags[4].get_text(strip=True)
        
        timestamp = datetime.datetime.now()

        fashion = {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp
        }

        return fashion
    
    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return None


def scrape_fashion(base_url, start_page=2, delay=2):
    """
    Scrape fashion product data from multiple pages of the given website.

    This function iterates through pages starting from the base URL,
    extracts all product details, and returns them as a list of dictionaries.
    A delay between requests is applied to avoid overwhelming the server.

    Args:
        base_url (str): The base URL of the website to scrape.
        start_page (int, optional): The page number to start scraping 
            from. Defaults to 2.
        delay (int, optional): Delay in seconds between page requests.
            Defaults to 2.

    Returns:
        list[dict] | None: A list of extracted fashion product data if 
        successful, otherwise None.
    """
    data = []
    try:
        url = base_url
        print(f"Scraping pages: {url}")
        
        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            product_details = soup.find_all("div", class_="product-details")
            for product in product_details:
                fashion = extract_fashion_data(product)
                data.append(fashion)
        
        time.sleep(delay)

        page_number = start_page
        next_page_url = base_url + "page{}"
        
        while True:
            url = next_page_url.format(page_number)
            print(f"Scraping pages: {url}")

            content = fetching_content(url)
            if content:
                soup = BeautifulSoup(content, "html.parser")
                product_details = soup.find_all("div", class_="product-details")
                for product in product_details:
                    fashion = extract_fashion_data(product)
                    data.append(fashion)
                
                next_button = soup.find("li", class_="page-item next")
                if next_button:
                    page_number += 1
                    time.sleep(delay)
                
                else:
                    print("Couldn't find the next button")
                    break
            
            else:
                print("Content not found")
                break

        return data
    
    except Exception as e:
        print(f"Error saat menggambil seluruh data: {e}")
        return None

