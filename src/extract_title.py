def extract_title(markdown: str):
    lines = markdown.split('\n')
    header_found = False
    for line in lines:
        line = line.strip()
        if line[0:2] == '# ':
            header_found = True
            break

    if header_found:
        return line[2:]
    else:
        raise Exception("Markdown does not contain first-level header")
    
