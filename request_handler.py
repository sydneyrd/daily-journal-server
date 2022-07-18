from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import get_all_entries, get_single_entry, delete_entry, get_search_entry, create_new_entry, get_all_moods, update_entry, get_all_tags, get_all_entrytags
import json



# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 
                        'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                        'X-Requested-With, Content-Type, Accept')
        self.end_headers()
    
    
    def parse_url(self):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(self.path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def do_GET(self):
        self._set_headers(200)
        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url()
        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "moods":
                response = f"{get_all_moods()}"

            if resource == "journalentries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
            if resource == "tags":
                response = f"{get_all_tags()}"
            if resource == "entrytags":
                response = f"{get_all_entrytags()}"
        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed
            if query.get('q') and resource == "journalentries":
                response = get_search_entry(query['q'][0])
        self.wfile.write(response.encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url()

    # Delete a single animal from the list
        if resource == "journalentries":
            delete_entry(id)

    # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url()
        # Initialize new animal
        new_entry = None
        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "journalentries":
            new_entry = create_new_entry(post_body)
            self.wfile.write(f"{new_entry}".encode())
    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id) = self.parse_url()

        success = False

        if resource == "journalentries":
            success = update_entry(id, post_body)
    # rest of the elif's
        #elif resource == "employees":
        #   success = update_employee(id, post_body)
        # elif resource == "customers":
        #     success = update_customer(id, post_body)
        # elif resource == "locations":
        #    success = update_location(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())



def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
