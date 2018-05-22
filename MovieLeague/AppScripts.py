class Scripts(object):
    def __init__(self):
        pass

    @staticmethod
    def convert_dollar_to_int(dollar):
        if isinstance(dollar, str):
            dollar = dollar.replace("$", "")
            dollar = dollar.replace(",", "")
            return int(dollar)
        else:
            return 0

    @staticmethod
    def convert_int_to_dollar(dollar):
        return '${:,}'.format(dollar)


if __name__ == '__main__':
    print Scripts().convert_int_to_dollar(3453483881)