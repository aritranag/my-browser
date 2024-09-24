# implementing my own telnet

import socket
import ssl
import os

class URL:
    """
    URL class to work with a URL

    Method List:
    constructor - parses the URL string into scheme, host and path
    request - Creates a socket object to connect to the server and make a request call based on scheme, port and path. Returns the response as an object
    _requestFile - Utility function to support the file protocol, provides the directory listing for a path or the contents of the file
    _createRequest - Utility function to create the necessary request
    _parseResponse - Utility function to parse the response into an object format for later use
    """
    def __init__(self,url):
        """
        @param: url - URL of the website we are trying to go to / file url
        parses the URL into scheme/protocol,port, host and path. stores them as object properties
        For file url :- file:///path | file://localhost/path
        """
        self.scheme,url = url.split("://",1)
        
        #checking the fact that our browser only supports http / https / file
        assert self.scheme in ["http","https","file"]

        # add the / if not in the url, path is empty
        if "/" not in url:
            url = url + "/"

        # getting the host and the path
        self.host, url = url.split("/",1)

        #get the port if defined in the URL, else assign default ports
        if ":" in self.host:
            self.host, self.port = self.host.split(":",1)
            self.port = int(self.port)
        else:
            if self.scheme == "http":
                # 80 is the http default port
                self.port = 80
            elif self.scheme == "https":
                # 443 is the https default port
                self.port = 443
            elif self.scheme == "file":
                # file url is of the format file:///path | file://hostname/path, file will have no port
                self.port = None
    
        self.path = "/" + url


    def request(self):
        """
        Download the web page defined by the host and path values in the class object
        For the file protocol serve the directory or the file defined in path

        Response:-
        For http / https scheme - Dictionary object with the following keys
            version : Version of the protocol being used
            status : status code of the response
            explanation : Explanation of the status code
            response_headers : {dictionary with all the headers as key-value pairs}
            content : body of the response
        For file scheme - dict object
            content : Content of the file / listing of the directory being requested
        """
        if self.scheme == "file":
            return self._requestFile()
        
        # create a socket to connect to the host 
        # socket connection details = family=address family, defines location(where), type=stream/datagran(what), proto=(how)
        s = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM,proto=socket.IPPROTO_TCP)
        
        #TODO: create different instances of the socket connection string for different types and protocol

        # connect to the host using the hostname and the port
        s.connect((self.host,self.port)) # connect accepts a single argument with all the params defined

        # wrap it in a ssl context to establish a secure connection for the https protocol
        if self.scheme == "https":
            _ctx = ssl.create_default_context()
            s = _ctx.wrap_socket(s,server_hostname=self.host)

        request = self._createRequest()
        s.send(request.encode('utf8')) #encode the request in utf8 format to create a byte stream to send
        #TODO : understand the nuances of the encoder to use for real world use case

        #RESPONSE from the server
        # originally we have to use a loop to read all the bytes coming to the socket from the server
        # makefile utility in python is a shortcut to read all the bytes, decode it in the proper format and even accommodate HTTP line endings
        response = s.makefile('r',encoding="utf8",newline="\r\n")
        responseObj = self._parseResponse(response)
        s.close()

        return responseObj
    

    def _requestFile(self):
        """
        Serves up the file as defined by the path in the file url, or the listing for a directory

        Response:
        The file object or the directory listing defined in path
        """
        _r = {}
        #default path = /
        if os.path.exists(self.path):
            # since path exists determine whether it is a directory or a file and send response accordingly
            if os.path.isfile(self.path):
                # TODO : serve up the file in bytes and figure out how to show it in browser
                _r["content"] = "this is a file"
            elif os.path.isdir(self.path):
                # serve up the contents of the directory as a list of strings
                _r["content"] = "\n".join(os.listdir(self.path))
            else:
                _r["content"] = "Neither file nor path, error"

        return _r

    def _createRequest(self):
        """
        Create request string to send to the server

        Response:
        request - Complete Request string with all the headers added
        """
        # REQUEST being created for sending
        #GET path HTTP/1.0
        #Host: hostname
        #User-Agent : python/3
        #Connection : Close
        #empty line to indicate end of the input
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "User-Agent: {}\r\n".format("python/3")
        request += "Connection: close\r\n"
        request += "\r\n"
        return request
    

    def _parseResponse(self,response):
        """
        Utility function for parsing the response (response must be a an object of makefile)
        Creates a dictionary with all the parts of the response and returns it
        """
        _r = {}

        #1st line of the response is the status line containing version,status,explanation
        statusLine = response.readline()
        _r["version"],_r["status"],_r["explanation"] = statusLine.strip().split(" ",2)

        # Headers section
        # loop through the next lines until there is an empty line
        _r["response_headers"] = {}
        while True:
            _line = response.readline()
            if _line == "\r\n": break
            header, value = _line.split(":",1)
            _r["response_headers"][header.casefold()] = value.strip() # casefold => convert to lowercase

        #couple of asserts to check for a few headers
        assert "transfer-encoding" not in _r["response_headers"]
        assert "content-encoding" not in _r["response_headers"]

        # Body
        # everything remaining is the body
        _r["content"] = response.read()

        return _r

                                        
def load(url):
    """
    Requests the URL and then calls show to print the text returned, for file protocol simply prints the content
    """
    newUrl = URL(url)
    response = newUrl.request()
    if newUrl.scheme == "file":
        print(response["content"])
    else:
        show(response["content"])

def show(body):
    """
    A simple HTML parser, shows all the text in the HTML, but none of the tags
    """
    _in_tag = False
    # goes through each character in the body
    # determines whether the character is part of a tag
    # if not, the character is printed
    for c in body:
        if c == '<':
            _in_tag = True
        elif c == '>':
            _in_tag = False
        elif not _in_tag:
            print(c,end="")


