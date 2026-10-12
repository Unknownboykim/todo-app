# Experiment 4: the `webbrowser` module — open URLs in the user's
# default browser.
#
# Combined with f-strings, you can build a "search Google for this"
# tool: take the user's term, plug it into Google's search URL, and
# open the result page.

# 147. Code Experiments - Experiment 4 (Section 15)
# Experiment 4: the `webbrowser` module — open URLs in the user's
# default browser.
# Combined with f-strings, you can build a "search Google for this"
# tool: take the user's term, plug it into Google's search URL, and
# open the result page.

import webbrowser   # standard module


search_term = input("Enter a search term: ")

# In a URL, spaces are written as "+" (the lecture's version):
#   "python modules" -> "python+modules"
search_term = search_term.replace(" ", "+")

webbrowser.open(f"https://google.com/search?q={search_term}")
