#!/usr/bin/python3

"""
Miguel Ángel Lozano Montero.
Program implementing a commented content cache.
"""

import webapp
import urllib.request


class contentCache (webapp.webApp):
    """Web application that works as a content cache
    with links to the original page and to reload the page."""

    cache = {}

    def parse(self, request):
        """Return the method and the resource name (with /)"""

        lista = request.split()
        method = lista[0]
        resourceName = lista[1]

        return (method, resourceName)

    def process(self, parsed):
        """Process the relevant elements of the request. """

        method, resourceName = parsed

        if method == "GET":
            if resourceName.startswith('/reload'):
                parsedResourceName = resourceName[7:]
                httpCode = "200 OK"
                htmlBody = "<meta http-equiv='refresh'" + \
                           "content='0;url=" + parsedResourceName + "'>"
            else:
                if resourceName in self.cache.keys():
                    httpCode = "200 OK"
                    htmlBody = self.cache[resourceName]
                else:
                    url = "http:/" + resourceName
                    try:
                        f = urllib.request.urlopen(url)
                        htmlBody = f.read().decode('utf-8')
                        pos_start_body = htmlBody.find('<body')
                        pos_end_body = htmlBody.find('>', pos_start_body)
                        before = htmlBody[:pos_end_body + 1]
                        after = htmlBody[pos_end_body + 1:]
                        menu = "<h1><a href=" + url + ">" + \
                               "Enlace original</a><br/>" + \
                               "<a href=/reload" + resourceName + \
                               ">Recarga</a></h1>"
                        htmlBody = before + menu + after
                        httpCode = "200 OK"
                        self.cache[resourceName] = htmlBody
                    except OSError:
                        httpCode = "404 Not Found"
                        htmlBody = ""
                    except UnicodeDecodeError:
                        print("Impossible to decode an element")
                        httpCode = "404 Not Found"
                        htmlBody = ""
        else:
            httpCode = "405 Method Not Allowed"
            htmlBody = "<html><body><h1>" + "Recurso no permitido" + \
                       "</h1></body></html>"

        return (httpCode, htmlBody)


if __name__ == "__main__":
    testContentCache = contentCache("localhost", 1234)
