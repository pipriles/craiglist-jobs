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
    '"Dental Assistant"'
]

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
 ]

CREDS_JSON = os.getenv('CREDS_FILE')
if not CREDS_JSON:
    CREDS_JSON = './creds.json'

SHEET_KEY  = os.getenv('GSHEETS_KEY')

def main():
    pass

if __name__ == '__main__':
    main()

