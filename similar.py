import difflib

def not_similar(str_a, list):
    
    if len(list) < 1:
        return True
    
    for str_b in list:
        match = difflib.SequenceMatcher(None, str_a, str_b).ratio()
        print (match)
        if match > 0.85:
            print ("false")
            return False

    print ("true")
    return True
        
