from rdflib import Graph
from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD
import gspread
from gspread.exceptions import CellNotFound
import webbrowser
import httplib2
from oauth2client import client

# Authenticate with Google Services
flow = client.flow_from_clientsecrets(
   'secret.json',
   scope='https://spreadsheets.google.com/feeds',
   redirect_uri='urn:ietf:wg:oauth:2.0:oob')
auth_uri = flow.step1_get_authorize_url()
webbrowser.open(auth_uri)
auth_code = raw_input('Enter the auth code: ')
credentials = flow.step2_exchange(auth_code)
http_auth = credentials.authorize(httplib2.Http())

# Open Google Sheet
gc = gspread.authorize(credentials)
sheet = gc.open("OOSTT Sheet Test").sheet1

# SPARQL node : column heading
nodes = {
   'term': 'Term',
   'genus': 'Definition (genus differentia)',
   'userdef': 'rdfs:comment (user-centered definitions)'
}

# Only uncomment next 2 lines if creating new sheet:
# sheet.resize(1)
# sheet.append_row(nodes.values())
sheet_row = sheet.row_count  # number rows before writing to sheet

# Load OOSTT Ontology
g = Graph()
g.parse('https://raw.githubusercontent.com/OOSTT/OOSTT/master/oostt.owl', format='xml')

# Run SPARQL query & write results to appropriate columns
for row in g.query(
       """PREFIX obo: <http://purl.obolibrary.org/obo/>
    SELECT ?term ?genus ?userdef
    WHERE {
      ?class rdf:type owl:Class .
      ?class rdfs:label ?term .
      OPTIONAL {?class obo:IAO_0000115 ?genus .}
      OPTIONAL {?class obo:OOSTT_00000030 ?userdef .}
    }
     """):
   try:
       sheet_row = sheet.find(str(row['term'])).row
   except CellNotFound:
       sheet_row = sheet.row_count + 1
       sheet.add_rows(1)
   for node in nodes:
       sheet.update_cell(sheet_row, sheet.find(nodes[node]).col, row[node])
