#!/usr/bin/env python3

import os

# Complete keywords
KEYWORDS = [
    'Dentist',
    'Anesthesiologist',
    'Exodontist',
    'Endodontist',
    'Implantologist',
    'Orthodontist',
    'Pedodontist',
    'Prosthodontist',
    'Periodontist',
    '"Oral Surgeon"',
    '"Dental Anesthesiologist"',
    '"Dental Assistant"',
    '"Dental Hygienist"',
    '"Dental Specialist"',
    '"Dental Office Manager"',
    '"General Practitioner Implantologist"',
    '"General Practitioner Endodontist"',
    '"General Practitioner Prosthodontist"'
]

# Specialist keywords
SPECIALIST = [
    'Anesthesiologist',
    'Exodontist',
    'Endodontist',
    'Implantologist',
    'Orthodontist',
    'Pedodontist',
    'Prosthodontist',
    'Periodontist',
    '"Oral Surgeon"',
    '"Dental Specialist"',
    '"Dental Anesthesiologist"',
    '"General Practitioner Implantologist"',
    '"General Practitioner Endodontist"',
    '"General Practitioner Prosthodontist"'
]

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

US_STATES = {
    'arizona': 'AZ',
    'california': 'CA',
    'colorado': 'CO',
    'delaware': 'DE',
    'georgia': 'GA',
    'illinois': 'IL',
    'louisiana': 'LA',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'missouri': 'MO',
    'new jersey': 'NJ',
    'new york': 'NY',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'rhode island': 'RI',
    'texas': 'TX',
    'utah': 'UT',
    'virginia': 'VA',
    'washington': 'WA'
}

CL_STATES = [
    'washington',
    'michigan',
    'arizona',
    'new jersey',
    'delaware',
    'california',
    'ohio',
    'utah',
    'illinois',
    'missouri',
    'louisiana',
    'mass',
    'rhode island',
    'pennsylvania',
    'colorado',
    'georgia',
    'minnesota',
    'texas',
    'virginia',
    'new york',
    'oklahoma',
    'oregon'
]

CREDS_JSON = os.getenv('CREDS_FILE')
if not CREDS_JSON:
    CREDS_JSON = './creds.json'

SHEET_KEY  = os.getenv('GSHEETS_KEY')

def main():
    pass

if __name__ == '__main__':
    main()

