from ratelimiter import RateLimiter
from bs4 import BeautifulSoup
from typing import List
import wikipediaapi
import requests
import wiki_db
import time

rate_limit = RateLimiter(max_calls=100, period=60)
links_per_page = 200
duplicates = []
retry = 5

class WikiRacer:

    @rate_limit
    def main_parser(self, start_page):
        """"
        A function for parsing the main wikipedia pages and 
        getting all the tags 'a' from the page, returning this value 
        for further processing.
        """
        response = requests.get(start_page)
        soup = BeautifulSoup(response.text, "lxml")
        main_block = soup.find("div", class_="vector-body")
        a_tags = main_block.find_all("a", class_="")
        return a_tags

    def incoming_pages(self, article_name):
        """
        The function responsible for following the prepared link and 
        parsing the number of articles that have a link to the current one.
        """
        wiki = wikipediaapi.Wikipedia(
                language='uk',
                extract_format=wikipediaapi.ExtractFormat.WIKI
        )

        page_py = wiki.page(article_name)

        if page_py.exists():
            links = page_py.backlinks
            return len(links)

        else:
            return "0"

    def find_path(self, start_word: str, end_word: str) -> List[str]:
        """
        Basic function. In several runs searches for the shortest 
        route from the start word to the end word.
        """
        # Creating a database if it does not exist
        wiki_db.database_creation()

        # Checking the input data for availability in the database
        if wiki_db.database_checker(start_word, end_word):
            return wiki_db.database_checker(start_word, end_word)

        global retry
        return self.main_proccess(start_word, end_word, retry)

    def main_proccess(self, start_word, end_word, retry):
        # Creating a home page
        start_page = f"https://uk.wikipedia.org/wiki/{start_word}"

        # Checking the functionality of the page
        if requests.get(start_page).status_code == 200:
            global links_per_page
            global duplicates
            
            links_limiter = links_per_page
            duplicates.clear()
            urls_dict = {}

            # For TOP5 Page_IN's Block
            links_on_start_page = len(self.main_parser(start_page))
            links_on_end_page = len(self.main_parser(f"https://uk.wikipedia."
                                                     f"org/wiki/{end_word}"))

            # For TOP5 Page_OUT's Block
            start_word_out = self.incoming_pages(start_word)
            end_word_out = self.incoming_pages(end_word)

            # Main page tag traversal
            for a_tag_main in self.main_parser(start_page):
                if a_tag_main.get("title") in duplicates:
                    continue

                duplicates.append(a_tag_main.get("title"))
                if len(urls_dict) == links_per_page:
                    break

                elif a_tag_main.get("title") is None or ":" \
                        in a_tag_main.get("title"):
                    continue

                else:
                    urls_dict[a_tag_main.get("title")] = \
                        f"https://uk.wikipedia.org{a_tag_main.get('href')}"

                    if a_tag_main.get("title").lower() == end_word.lower():
                        page_titles = [start_word, end_word]

                        # Page_IN's Block
                        pages_in = [links_on_start_page, links_on_end_page]
                        max_links = max(pages_in)

                        # Page_OUT's Block
                        pages_out_list = [int(start_word_out), int(end_word_out)]
                        max_out_links = max(pages_out_list)

                        # Sending data to fill in the database
                        wiki_db.database_filling(
                            [start_word,
                             end_word,
                             page_titles[pages_in.index(max_links)],
                             max_links,
                             page_titles[pages_out_list.index(max_out_links)],
                             max_out_links]
                        )

                        # Return the path to the user
                        return [start_word, end_word]

            # Search for all filtered links on the main page
            for title, url in urls_dict.items():
                links_limiter = links_per_page

                # Second level page traversal
                for a_tag_second in self.main_parser(url):
                    if a_tag_second.get("title") in duplicates:
                        continue

                    duplicates.append(a_tag_second.get("title"))
                    if links_limiter <= 0:
                        break

                    elif a_tag_second.get("title") is None or ":" \
                            in a_tag_second.get("title"):
                        continue

                    elif a_tag_second.get("title").lower() == end_word.lower():
                        # For TOP5 (links on page)
                        links_on_middle_page = len(self.main_parser(
                            f"https://uk.wikipedia.org/wiki/{title}"))
                        middle_word_out = self.incoming_pages(title)

                        page_titles = [start_word, title, end_word]
                        # Page_IN's Block
                        pages_in = [links_on_start_page,
                                    links_on_middle_page,
                                    links_on_end_page]
                        max_links = max(pages_in)

                        # Page_OUT's Block
                        pages_out_list = [int(start_word_out),
                                     int(middle_word_out),
                                     int(end_word_out)]
                        max_out_links = max(pages_out_list)

                        # Sending data to fill in the database
                        wiki_db.database_filling(
                            [start_word,
                             title,
                             end_word,
                             page_titles[pages_in.index(max_links)],
                             max_links,
                             page_titles[pages_out_list.index(max_out_links)],
                             max_out_links])

                        # Return the path to the user    
                        return [start_word, title, end_word]

                    links_limiter -= 1

            # If at the end of the limit is 0 - the path is not found
            if links_limiter == 0:
                return []

        # The link failed verification. Outputting an error message
        else:
            if retry:
                time.sleep(1)
                print(f"[INFO] Try to connect to page №{retry} => {start_page}")
                return self.main_proccess(start_word, end_word, retry=(retry - 1))
            
            else:
                raise ValueError("[INFO] You have the wrong link in your data!")


print("[INFO] Wait for a search result\n")
