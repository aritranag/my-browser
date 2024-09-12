import sys

import url.myUrl as myUrl

urlString = "http://example.org/index.html"

def load(URL):
    '''
    Requests the URL and then calls show to print the text returned
    '''
    response = URL.request()
    URL.show(response["content"])

if __name__ == "__main__":
    load(myUrl.URL(sys.argv[1]))

    
