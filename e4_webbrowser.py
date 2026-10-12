# Experiment 4: the `webbrowser` module — open URLs in the user's
# default browser.
#
# Combined with f-strings, you can build a "search Google for this"
# tool: take the user's term, plug it into Google's search URL, and
# open the result page.

import webbrowser


search_term = input("Enter a search term: ")
webbrowser.open(f"https://google.com/search?q={search_term}")
