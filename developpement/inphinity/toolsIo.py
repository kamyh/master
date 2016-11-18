##
#   Created by: Deruaz Vincent
#   Input/Output tools
#   13.11.2016
##

from Logger import Logger


class ToolsIO:
    def __init__(self):
        self.LOGGER = Logger()

    def write(self, filename, txt):
        file = open(filename, "w+")
        file.write(txt)
        file.close()

    def read_results(self, filename, logged_detailed=False):
        file = open(filename, 'r')

        matching_lines = []
        lines = file.read().split('\n')
        self.LOGGER.log_debug('RESULTS: %s Hits (PF0XXXX)' % len(lines))

        for line in lines:
            if 'PF0' in line:
                self.LOGGER.log_detailed('%s ' % line, logged_detailed)
                matching_lines.append(line)

        return matching_lines