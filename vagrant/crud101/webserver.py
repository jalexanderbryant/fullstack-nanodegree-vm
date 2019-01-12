from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine
import cgi
import re

class webserverHandler(BaseHTTPRequestHandler):

    def _get_db_session(self):
        Base.metadata.bind = engine
        return sessionmaker(bind = engine)()

    def _send_200_OK(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _send_301_redirect(self):
        self.send_response(301)
        # self.send_response....
        self.end_headers()


    def do_GET(self):
        db_session = self._get_db_session()
        page_title = "Something something something"
        page_body = "This is a body"

        try:
            greeting = 'hello'

            if self.path.endswith('/restaurants'):
                page_title = "Restaurants"
                page_body = "This list of restaurants"
                query_results = db_session.query(Restaurant).all()
                list_of_restaurants = ""
                for e in query_results:
                    list_of_restaurants += "%s<br />\n" % e.name
                    list_of_restaurants += "<a href='/restaurants/%s/edit'>Edit</a><br/>" % e.id
                    list_of_restaurants += "<a href='/restaurants/%s/delete'>Delete</a>" % e.id
                    list_of_restaurants += "<br/><br/><br/>"
                page_body = list_of_restaurants
                self._send_200_OK()

            if self.path.endswith('/edit'):
                res_id = re.findall('\d+', self.path)[0]
                res = db_session.query(Restaurant).filter_by(id = int(res_id)).one()


                page_title="Edit Restaurant"
                page_body = "<html></body><h1>Rename Restaurant</h1>"
                page_body += "<h3>%s</h3>" % res.name
                page_body += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % res_id
                page_body += "<input type='text' name='restaurant_name' placeholder='New Restaurant Name'/>"
                page_body += "<input type='submit' name'Rename'/>"
                page_body += "</form></body></html>"

                print("debug123", res_id)
                print("debug2", )
                self._send_200_OK()

            if self.path.endswith('/delete'):
                res_id = re.findall('\d+', self.path)[0]
                res = db_session.query(Restaurant).filter_by(id = int(res_id)).one()
                page_title = "Delete Restaurant"
                page_body = "<html><body>"
                page_body += "<h1>Are you sure you want to delete %s?" % res.name
                page_body += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % res_id
                page_body += "<input type='submit' name'Confirm'/>"
                page_body += "</form></body></html>"
                self._send_200_OK()


            if self.path.endswith('/restaurants/new'):
                page_title = "New Restaurant"
                page_body = "<html></body><h1>Create a new Restaurant</h1>"
                page_body += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                page_body += "<input type='text' name='restaurant_name' />"
                page_body += "<input type='submit' name'Create'/>"
                page_body += "</form></body></html>"
                self._send_200_OK()

           



            output = """
            <html>
                <title>%s</title>
                <body>
                    %s
                </body>
            </html>
            """ % (page_title, page_body)

            self.wfile.write(output)
            # print(output)
            return

        except:
            self.send_error(404, "File Not Found %s" % self.path )

    def do_POST(self):
        db_session = self._get_db_session()

        try:
            # self.send_response(301)
            # self.end_headers()

            # Parse html form header into main value and dictionary parameters
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            
            if self.path.endswith('/restaurants/new'):
                print("Creating a new restaurant")

                # Check to see if the content type is form data
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    new_name = fields.get('restaurant_name')
                    print("New restaurant name:", new_name[0])
                    r = Restaurant(name = new_name[0])
                    db_session.add(r)
                    db_session.commit()

            if self.path.endswith('/edit'):
                print("Renaming a restaurant")

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    new_name = fields.get('restaurant_name')
                    print("New restaurant name:", new_name[0])

                    res_id = re.findall('\d+', self.path)[0]
                    print("Changing name for id: ", res_id)
                    res = db_session.query(Restaurant).filter_by(id = int(res_id)).one()
                    print("Restaurant queried:", res.name)
                    res.name = new_name[0]
                    db_session.add(res)
                    db_session.commit()

            if self.path.endswith('/delete'):
                print("Deleting a restaurant")
                res_id = re.findall('\d+', self.path)[0]
                print("id to delete: ", res_id)
                res = db_session.query(Restaurant).filter_by(id = int(res_id)).one()
                print("Name to delete: ", res.name)
                db_session.delete(res)
                db_session.commit()

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()
            
            
            
            

            # # output = ""
            # output += "<html><body>"
            # output += " <h2>Okay, how about this: </h2>"
            # output += "<h1> %s </h1>" % messagecontent[0]

            # output += "<form method='POST' enctype='multipart/form-data'"
            # output += "action='/hello'><h2>What would you like me to say?</h2>"
            # output += "<input name='message' type='text'><input type='submit'"
            # output += " value='Submit'></form>"

            # output += "</body></html>"
            # self.wfile.write(output)
            # print(output)
            return
        except:
            pass
    
def main():
    try:
        port = 8000
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s") % port
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
