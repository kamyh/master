##
#   Created by: Deruaz Vincent
#   Input/Output tools
#   13.11.2016
##

class ToolsIO:
    def __init__(self):
        pass

    def write(self, filename, txt):
        file = open(filename, "w+")
        file.write(txt)
        file.close()

    def read_results(self, filename):
        file = open(filename, 'r')

        matching_lines = []

        for line in file.read().split('\n'):
            if 'PF0' in line:
                matching_lines.append(line)

        return matching_lines