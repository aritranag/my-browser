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

# Project Structure of the Repo

# Testing

Create your own python server for testing using this command - python3 -m http.server 8000 -d /some/directory
Then use the localhost URL to test your code
