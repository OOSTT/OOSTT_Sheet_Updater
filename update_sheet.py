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

# only uncomment next 3 lines if creating new sheet:
# sheet.resize(1)
# heading = ["Term","Definition (genus differentia)","rdfs:comment(user-centered definitions)"]
# sheet.append_row(heading)

# Find out which column in sheet to place term & definitions
sheet_row = sheet.row_count  # number rows before writing to sheet
term = sheet.find("Term")
genus = sheet.find("Definition (genus differentia)")
userdef = sheet.find("rdfs:comment (user-centered definitions)")

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
   sheet_row += 1
   sheet.add_rows(1)
   sheet.update_cell(sheet_row, term.col, row['term'])
   sheet.update_cell(sheet_row, genus.col, row['genus'])
   sheet.update_cell(sheet_row, userdef.col, row['userdef'])
