import requests
from bs4 import BeautifulSoup
import json



# {
#     "title": "Introduction to Computer Science",
#     "code": "CSC108H1",
#     "year": 1,  // Derived from the course code
#     "description": "A basic introduction to programming and computer science...",
#     "embedding": [0.1, 0.2, ...],  // Embedding from SentenceTransformer
#     "related_courses": ["CSC148H1", "CSC165H1"],  // Optional: manually link related courses or based on NLP similarity
#     "prerequisites": ["None"]  // Prerequisite courses, scraped or derived
# }


def extract_year_from_code(course_code):
    """Extracts the year of the course based on the fourth character of the course code."""
    try:
        year_char = course_code[3]
        if year_char.isdigit():
            return int(year_char)
    except IndexError:
        pass
    return None  # Return None if year cannot be determined


def scrape_course_data():
    courses = []
    page = 0
    while True:
        url = f'https://artsci.calendar.utoronto.ca/search-courses?course_keyword=&field_section_value=Computer+Science&field_prerequisite_value=&field_breadth_requirements_value=All&page={page}'
        print(f'Scraping page {page}')
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Failed to retrieve page {page}. Status code: {response.status_code}')
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        course_rows = soup.find_all('div', class_='views-row')
        if not course_rows:
            print(f'No courses found on page {page}. Ending pagination.')
            break

        for course_row in course_rows:
            try:
                course_header = course_row.find('h3', class_='js-views-accordion-group-header')
                if not course_header:
                    continue

                title_div = course_header.find('div', attrs={'aria-label': True})
                if not title_div:
                    continue
                course_code_title = title_div.get('aria-label').strip()
                if ' - ' in course_code_title:
                    code, title = course_code_title.split(' - ', 1)
                else:
                    code, title = course_code_title, ''

                # Extract year from course code
                year = extract_year_from_code(code)

                # Get the course description
                content_div = course_row.find('div', class_='field-content')
                course_details = content_div.get_text(separator=' ', strip=True) if content_div else ''

                course = {
                    'title': title,
                    'code': code,
                    'description': course_details,
                    'year': year,  # Add the year field
                    'related_courses': [],  # You can add related courses in later processing
                }

                courses.append(course)

            except Exception as e:
                print(f"Error parsing course {course_code_title}: {e}")
                continue

        page += 1

    return courses

if __name__ == '__main__':
    courses = scrape_course_data()
    print(f"Scraped {len(courses)} courses.")
    file_name = 'cs_courses.json'
    with open(file_name, 'w') as file:
        json.dump(courses, file, indent=2)
