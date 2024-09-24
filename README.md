# Web Browser Implementation

[Book](https://browser.engineering/)

## Inversion of Control

The framework calls the custom code as necessary, in this case the web browser is the framework calling the event handling custom code defined by the user to handle specific user events.

## Syntax of URL's

http://example.org:80/index.html

http :- scheme; how to get the information  
80 :- port; defines the full adress with the hostname  
example.org :- hostname; where to get it  
index.html :- path; what to get

# Running the code

python3 index.py <url>

# Project Structure of the Repo

# Testing

Create your own python server for testing using this command - python3 -m http.server 8000 -d /some/directory
Then use the localhost URL to test your code

# Development Notes

1. Support for Http scheme - Initial
2. Support for Https scheme - 18/09/2024
3. Support for file scheme - 19/09/2024
4. Start the creation of the UI - 25/09/2024
