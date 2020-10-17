from bs4 import BeautifulSoup
import requests
import pandas as pd
from tabulate import tabulate
import re


# Write the contents of the url
def parser(url):
    # Check if the request was successful
    if requests.get(url).status_code == 200:
        # Store the contents of the url into a variable
        info = requests.get(url).content
        # Return the contents
        return BeautifulSoup(info, 'lxml')
    else:
        # Return a error
        return "Error 404 not found"


# Gets the table of information
def infotable(url):
    try:
        # Stores the info table in df
        df = pd.DataFrame(pd.read_html(url)[0])
        # Returns a formatted version of the table
        return tabulate(df, headers=["Questions", "Answers"], showindex=False, tablefmt="plain")
    except Exception as e:
        # Returns the error and prints it
        print(e, "Infotable")
        return "Error 404 not found!"


# Gets the string between the start and end
def section(start, end, string):
    return re.findall(f"{start}(.+?){end}", string)


# Gets the desired text
def webmachine(header, html):
    try:
        # Stores the information between two headers in a variable
        Xqc = section(f'<h2>{header}', r'<h2><span class="mw-headline"', str(html))
        # Turns the list into a string
        String = " ".join(Xqc)
        # Gets the desired text and returns it
        return " ".join(re.findall(r"(?:<p>(?:.+?)</p>)|(?:<li>(?:.+?)</li>)", String))
    except Exception as e:
        print(e, "Webmachine")
        return "Error 404 not found"


# Gets the image of the object
def Image(html):
    # Gets a list of images on the web page.
    images = html.find('div', class_="notaninfobox").findAll('img')
    # Gets the first one
    return images[0]['src']


# Basically gets the contents of the page and turns it into a string
def Conversion(html):
    return " ".join(str(html).split())


# Removes all the stuff in the <>
def clean(string):
    # Checks if string is empty
    if not string:
        return "Error 404 not found"
    else:
        # Returns a string with all of the stuff in <> replaced with nothing
        return re.sub("<.+?>", "", str(string))


# Loads all the headers into a dictionary
def load():
    # Creates a variable
    table = {}
    # Opens lookup.txt
    with open("lookup.txt", "r") as file:
        # For each line in the file
        for lines in file.readlines():
            # Split the lines, so it forms a array of words
            words = lines.split()
            # Key will be the first word, Value will be rest of the other words
            table[words[0]] = ' '.join(words[1:len(words)])
    # Returns the dictionary
    return table
