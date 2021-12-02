def parse_comma_string_to_int(string):
    '''
    used to convert comma seperated dollar to integer
    '''
    try:    
        number = int(string.replace(",", ""))
    except: number = 0
    return number

