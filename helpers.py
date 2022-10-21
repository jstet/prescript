def write_file(path, mode, content):
    f = open(path, mode)
    f.write(content)
    f.close()