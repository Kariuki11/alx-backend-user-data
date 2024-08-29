import re

def filter_datum(fields, redaction, message, separator):
    return re.sub(rf'({"|".join(fields)})=[^{separator}]+', lambda m: f'{m.group(1)}={redaction}', message)
