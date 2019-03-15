class read_large_file:

    def __init__(self):
        self.file_path = "large_file.txt"

    def get_file(self):
        with open(self.file_path, 'rb') as f:
            while(True):
                content = f.read(16)
                if content:
                    yield content
                else:
                    return


class write_largge_file:

    def __init__(self):
        self.file_path = "large_file_write.txt"
        self.f = open(self.file_path, "a+")

    def write_to_file(self, data):
        self.f.write(data)
        




if __name__ == "__main__":
    test = read_large_file()
    for content in test.get_file():
        print(content)