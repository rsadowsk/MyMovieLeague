from itsdangerous import URLSafeSerializer
from MovieLeague import app
import re, htmlentitydefs


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

    @staticmethod
    def token_dump(data):
        return URLSafeSerializer(app.config["SECRET_KEY"]).dumps(data)

    @staticmethod
    def token_load(token):
        return URLSafeSerializer(app.config["SECRET_KEY"]).loads(token)

    @staticmethod
    def fix_acii(text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text  # leave as is

        return re.sub("&#?\w+;", fixup, text)

    @staticmethod
    def fix_unicode(text):
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)




if __name__ == '__main__':
    print Scripts().fix_acii('The Gospel According to Andr\xe9')
