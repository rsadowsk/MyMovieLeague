class Scripts(object):
    def __init__(self):
        pass

    def convert_dollar_to_int(self, dollar):
        if isinstance(dollar, str):
            dollar = dollar.replace("$", "")
            dollar = dollar.replace(",", "")
            return int(dollar)
        else:
            return 0

    def convert_int_to_dollar(self, dollar):
        if isinstance(dollar, int):
            return '${:,}'.format(dollar)
        else:
            return None


if __name__ == '__main__':
    print Scripts().convert_dollar_to_int('$7,111')