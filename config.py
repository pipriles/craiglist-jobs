#!/usr/bin/env python3

import os

KEYWORDS = [
    'Orthodontist',
    'Oral Surgeon',
    'Periodontist', 
    'Endodontist',
    'Pedodontist',
    '"Dental Specialist"',
    '"Dental Anesthesiologist"',
    'Prosthodontist',
    'Dentist',
    '"Dental Hygienist"',
    '"Dental Assistant"',

    # New
    'OS',
    'Implantologist',
    'Perio',
    'Exo',
    'Endo',
    'Ortho',
    '"GP Prostho"',
    '"GP Implantologist"',
    '"GP Endo"',
    'Anesthesiologist',
]

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

STATES = [
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

