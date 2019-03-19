class read_large_file:

    def __init__(self):
        self.file_path = "large_file.txt"
        self.file_path = "large_file_write.txt"
        self.new_f = open(self.file_path, "r")

    def get_file(self):
        with open(self.file_path, 'rb') as f:
            while(True):
                content = f.read(16)
                if content:
                    yield content
                else:
                    return
            '''
            for line in f:
                if line:
                    yield line
                else:
                    return
            '''

    def write_to_file(self, data):
        self.new_f.write(data)


if __name__ == "__main__":
    test = read_large_file()
    i = 0
    for content in test.get_file():
        i = i + 1
        test.write_to_file(content)
        print i
        
    test.new_f.close()
