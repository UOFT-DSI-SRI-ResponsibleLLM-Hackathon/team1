import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time  # For adding delays between requests
# import nltk
# from sentence_transformers import SentenceTransformer
from mongodb.splitter import save_json

# nltk.download('punkt')


def scrape_course_data():
    """
    Scrape course data from the university website and return a list of course dictionaries.
    """
    courses = []
    page = 0
    while True:
        # Construct the URL for the current page
        url = f'https://artsci.calendar.utoronto.ca/search-courses?course_keyword=&field_section_value=All&field_prerequisite_value=&field_breadth_requirements_value=All&page={page}'
        print(f'Scraping page {page}')
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Failed to retrieve page {page}. Status code: {response.status_code}')
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all course containers
        course_rows = soup.find_all('div', class_='views-row')
        if not course_rows:
            print(f'No courses found on page {page}. Ending pagination.')
            break

        for course_row in course_rows:
            try:
                # Get the course header
                course_header = course_row.find('h3', class_='js-views-accordion-group-header')
                if not course_header:
                    continue

                # Extract course code and title
                title_div = course_header.find('div', attrs={'aria-label': True})
                if not title_div:
                    continue
                course_code_title = title_div.get('aria-label').strip()
                if ' - ' in course_code_title:
                    code, title = course_code_title.split(' - ', 1)
                else:
                    code = course_code_title
                    title = ''

                # Get the course content
                content_div = course_row.find('div', class_='field-content')
                course_details = content_div.get_text(separator=' ', strip=True) if content_div else ''

                # Create a course dictionary
                course = {
                    'title': title,
                    'code': code,
                    'description': course_details
                }

                courses.append(course)

            except Exception as e:
                print(f"Error parsing course {course_code_title}: {e}")
                continue

        # Go to the next page
        page += 1

    return courses


if __name__ == '__main__':
    courses = scrape_course_data()
    print(f"Scraped {len(courses)} courses.")
    save_json(courses, 'courses.json')
