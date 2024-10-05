import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient, errors
import time

def scrape_club_data():
    """
    Scrape student clubs data from the university website and return a list of club dictionaries.
    Handles pagination by iterating through pages until no more clubs are found.
    """
    base_url = 'https://sop.utoronto.ca/groups/'
    params = {
        'pg': 0  # Starting page number
    }
    
    headers = {
        'User-Agent': 'ClubScraperBot/1.0 (your_email@example.com)'  # Replace with your contact info
    }
    
    clubs = []
    session = requests.Session()
    session.headers.update(headers)
    
    while True:
        url = f"{base_url}?pg={params['pg']}"
        print(f"Scraping page {params['pg']} - URL: {url}")
        
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve page {params['pg']}. Error: {e}")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all club list items
        club_items = soup.find_all('li', class_='flex gap-8')
        print(len(club_items))
        if not club_items:
            print(f"No clubs found on page {params['pg']}. Ending pagination.")
            break  # Exit loop if no clubs are found
        
        for item in club_items:
            try:
                # Extract club information
                club_info = item.find('span', class_='flex-1 flex gap-4')
                if not club_info:
                    print("Club info span not found. Skipping this club.")
                    continue
                
                # Opportunity Name and Link
                opportunity_link_tag = club_info.find('a', class_='font-bold text-primary')
                if opportunity_link_tag:
                    opportunity_name = opportunity_link_tag.get_text(strip=True)
                    opportunity_link = opportunity_link_tag.get('href', '').strip()
                    # Ensure the link is absolute
                    if not opportunity_link.startswith('http'):
                        opportunity_link = f"https://sop.utoronto.ca{opportunity_link}"
                else:
                    opportunity_name = ''
                    opportunity_link = ''
                
                # Club Name and Link
                club_link_tag = club_info.find('a', class_='inline-flex bg-slate-100 py-1 px-2 rounded')
                if club_link_tag:
                    club_name = club_link_tag.get_text(strip=True)
                    club_link = club_link_tag.get('href', '').strip()
                    # Ensure the link is absolute
                    if not club_link.startswith('http'):
                        club_link = f"https://sop.utoronto.ca{club_link}"
                else:
                    club_name = ''
                    club_link = ''
                
                # Location
                location_tag = item.find_all('span')
                if len(location_tag) >= 2:
                    location = location_tag[1].get_text(strip=True)
                else:
                    location = ''
                
                # Description
                description = scrape_opportunity_description(opportunity_link, session)
                
                # Create a club dictionary
                club = {
                    'opportunity_name': opportunity_name,
                    'opportunity_link': opportunity_link,
                    'club_name': club_name,
                    'club_link': club_link,
                    'location': location,
                    'description': description
                }
                
                clubs.append(club)
                print(f"Scraped club: {club_name} - {opportunity_name}")
                
                # Optional: Add a short delay between requests to avoid overwhelming the server
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error parsing club: {e}")
                continue
        
        # Move to the next page
        params['pg'] += 1
        
        # Optional: Add a delay between page requests
        time.sleep(1)
    
    return clubs

def scrape_opportunity_description(url, session):
    """
    Scrape the description from the opportunity page.
    
    Args:
        url (str): URL of the opportunity page.
        session (requests.Session): Requests session with headers.
    
    Returns:
        str: Description text of the opportunity.
    """
    if not url:
        return ''
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve opportunity page at {url}. Error: {e}")
        return ''
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Adjust the selector based on the actual HTML structure of the description
    # Example: description might be within a div with class 'description' or similar
    description_div = soup.find('div', class_='description')  # Example selector
    if not description_div:
        # Try alternative selectors if necessary
        description_div = soup.find('div', class_='wysiwyg')  # Another example
    
    if description_div:
        # Clean the description text
        description = description_div.get_text(separator=' ', strip=True)
    else:
        description = ''
    
    return description

def insert_clubs_into_db(clubs):
    """
    Insert a list of clubs into the MongoDB database.
    Uses upsert to avoid duplicates based on 'opportunity_link'.
    
    Args:
        clubs (list): List of club dictionaries.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')  # Replace if your MongoDB is hosted elsewhere
        db = client['university_clubs']
        clubs_collection = db['clubs']
        
        # Create a unique index on 'opportunity_link' to prevent duplicates
        try:
            clubs_collection.create_index('opportunity_link', unique=True)
        except errors.OperationFailure as e:
            print(f"Index creation failed: {e}")
        
        for club in clubs:
            try:
                clubs_collection.update_one(
                    {'opportunity_link': club['opportunity_link']},
                    {'$set': club},
                    upsert=True
                )
                print(f"Inserted/Updated club: {club['club_name']} - {club['opportunity_name']}")
            except errors.DuplicateKeyError:
                print(f"Duplicate club found: {club['club_name']} - {club['opportunity_name']}")
            except Exception as e:
                print(f"Error inserting club into DB: {e}")
        
        print(f"Total clubs inserted/updated: {len(clubs)}")
    
    except Exception as e:
        print(f"Failed to connect to MongoDB. Error: {e}")

if __name__ == '__main__':
    clubs = scrape_club_data()
    if clubs:
        insert_clubs_into_db(clubs)
    else:
        print('No clubs were scraped.')
