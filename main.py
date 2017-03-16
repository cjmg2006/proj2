#!/usr/bin/env python 
import OpenSSL 
import sys, getopt 
import socket 
import urlparse  

long_options = [     "tlsv1.0",     "tlsv1.1",     "tlsv1.2",     "sslv3",     "ciphers=",     "crlfile=",     "cacert=",     "allow-stale-certs=",     "pinnedcertificate=" ]  
short_options = "3"  
CRLF = "\r\n\r\n"  

def parse_url(url):     
	u = urlparse.urlparse(url)     
	scheme = u.scheme      
	host = u.netloc     
	port = 443     
	if ":" in host:         host, port = host.split(":")         port = int(port)      index = url.find(u.netloc) + len(u.netloc)     request_uri = url[index:]      return scheme, host, port, request_uri   def scurl(url, opts):     print "scurl: %s" % url      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      scheme, host, port, request_uri = parse_url(url)     print "Parsed:", scheme, host, port, request_uri      request = "GET %s HTTP/1.0%s" % (request_uri, CRLF)     print "Request: %s" % request      if scheme != "https":         print >> sys.stderr, "URL scheme must be https"         sys.exit(1)      ctx = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD) 
 	for opt, arg in opts:         pass      conn = OpenSSL.SSL.Connection(ctx, s)     conn.connect((host, port))      # Handshake     print "Doing handshake..."     conn.do_handshake()      conn.sendall(request)      data = []     try:         while 1:             data.append(conn.recv(1024))     except OpenSSL.SSL.ZeroReturnError:         pass
     data = "".join(data)     print data      print "\n\n\nShutting down..."     conn.shutdown()     print "Closing connection..."     conn.close()     print "Connection successfully closed."   def main(argv):     try:         opts, urls = getopt.getopt(argv, short_options, long_options)     except getopt.GetoptError as err:         print str(err)         sys.exit(2)     for url in urls:         scurl(url, opts)   if __name__ == "__main__":     main(sys.argv[1:])
