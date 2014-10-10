def clean_response(text):
    lines = text.split('\n')
    return '\n'.join([line for line in lines
                      if line.startswith('Night') or line.startswith('20')])
