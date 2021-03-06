import re
import tld

RE_DOMAIN = re.compile(
    r'(?:'
        r'\S+'
        r'(?'
            r'::\S*'
        r')?'
        r'@'
    r')?'
    r'(?:'
        r'(?!'
            r'10'
            r'(?:'
                r'\.\d{1,3}'
            r'){3}'
        r')'
        r'(?!'
            r'127'
            r'(?:'
                r'\.\d{1,3}'
            r'){3}'
        r')'
        r'(?!'
            r'169\.254'
            r'(?:'
                r'\.\d{1,3}'
            r'){2}'
        r')'
        r'(?!'
            r'192\.168'
            r'(?:'
                r'\.\d{1,3}'
            r'){2}'
        r')'
        r'(?!'
            r'172\.'
            r'(?:'
                r'1[6-9]'
                r'|'
                r'2\d'
                r'|'
                r'3[0-1]'
            r')'
            r'(?:'
                r'\.\d{1,3}'
            r'){2}'
        r')'
        r'(?:'
            r'[1-9]\d?'
            r'|'
            r'1\d\d'
            r'|'
            r'2[01]\d'
            r'|'
            r'22[0-3]'
        r')'
        r'(?:'
            r'\.'
            r'(?:'
                r'1?\d{1,2}'
                r'|'
                r'2[0-4]\d'
                r'|'
                r'25[0-5]'
            r')'
        r'){2}'
        r'(?:'
            r'\.'
            r'(?:'
                r'[1-9]\d?'
                r'|'
                r'1\d\d'
                r'|'
                r'2[0-4]\d'
                r'|'
                r'25[0-4]'
            r')'
        r')'
        r'|'
        r'(?:'
            r'(?:'
                r'[a-z\xa1-\xff0-9]+-?'
            r')*'
            r'[a-z\xa1-\xff0-9]+'
        r')'
        r'(?:\.'
            r'(?:'
                r'[a-z\xa1-\xff0-9]+-?'
            r')*'
            r'[a-z\xa1-\xff0-9]+'
        r')*'
        r'(?:\.'
            r'(?:'
                r'[a-z\xa1-\xff]{2,}'
            r')'
        r')'
    r')'
    r'(?:'
        r':\d{2,5}'
    r')?'
)

def domains(text):
    '''Extracts domain names from a corpus of text'''
    domains = set()
    for domain in RE_DOMAIN.findall(text):
        if tld.get_tld('http://{}'.format(domain)):
            domains.add(domain)
    return domains