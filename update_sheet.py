from rdflib import Graph
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

# Load OOSTT Ontology
g = Graph()
g.parse('https://raw.githubusercontent.com/OOSTT/OOSTT/master/oostt.owl', format='xml')
