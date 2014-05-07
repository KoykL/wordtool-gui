__author__ = 'sakuratanoshiminaki'
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from retrying import retry

KEY = "01C57073FFB5472B45411DF15B827A11"

@retry(wait='fixed_sleep', wait_fixed=2000, stop='stop_after_attempt', stop_max_attempt_number = 7)
def get_definition(word):
    query = {
        "w": word,
        "key": KEY
    }
    query_str = urllib.parse.urlencode(query)
    with urllib.request.urlopen("http://dict-co.iciba.com/api/dictionary.php?{query_str}".format(query_str=query_str)) as f:
        soup = BeautifulSoup(f.read(-1), "xml")
        return ["".join(element.stripped_strings) for element in soup.select("acceptation")]