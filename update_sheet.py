from rdflib import Graph
from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD
import gspread
import webbrowser
import httplib2
from oauth2client import client

# Authenticate with Google Services
flow = client.flow_from_clientsecrets(
       'secret.json',
        scope = 'https://spreadsheets.google.com/feeds',
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')
auth_uri = flow.step1_get_authorize_url()
webbrowser.open(auth_uri)
auth_code = raw_input('Enter the auth code: ')
credentials = flow.step2_exchange(auth_code)
http_auth = credentials.authorize(httplib2.Http())

# Open Google Sheet
gc = gspread.authorize(credentials)
sheet = gc.open("OOSTT Sheet Test").sheet1
sheet.resize(1)
heading = ["Class","Definition","User-Centered Description"]
sheet.append_row(heading)

# Load OOSTT Ontology
g = Graph()
g.parse('https://raw.githubusercontent.com/OOSTT/OOSTT/master/oostt.owl', format='xml')

cdd = g.query(
    """PREFIX obo: <http://purl.obolibrary.org/obo/>
        SELECT DISTINCT ?label ?definition ?description
        WHERE {
          ?class rdfs:label ?label.
          ?class obo:IAO_0000115 ?definition.
          ?class obo:OOSTT_00000030 ?description
        }""")

for row in cdd:
    sheet.append_row(row)
