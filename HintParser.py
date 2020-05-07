import re

class HintParser:
    fmt = "^\\[\\[\\[[1-9]*[0-9](,[1-9]*[0-9])*\\](,\\[[1-9]*[0-9](,[1-9]*[0-9])*\\])*\\],\\[\\[[1-9]*[0-9](,[1-9]*[0-9])*\\](,\\[[1-9]*[0-9](,[1-9]*[0-9])*\\])*\\]\\]$"

    @staticmethod
    def parseFile(filename):
        try:
            f = open(filename)
            h = f.readlines()
            f.close()
        except IOError:
            raise IOError("Problem z odczytaniem danych z pliku: %s" % filename)
        return HintParser.parseString(''.join(h))

    @staticmethod
    def parseString(s):
        s = ''.join(s.split())
        if not re.match(HintParser.fmt, s):
            raise Exception("Dane z pliku %s nie są poprawnie wprowadzone zgodnie z: %s" % (s, HintParser.fmt))
        p = s.split(']],[[')
        p[0] = p[0].lstrip('[[[')
        p[1] = p[1].rstrip(']]]')
        hr = [[int(y) for y in x.split(',')] for x in p[0].split('],[')]
        hc = [[int(y) for y in x.split(',')] for x in p[1].split('],[')]
        if sum(sum(hc,[])) != sum(sum(hc,[])):
            raise Exception("Niepoprawne wskazówki - wartości w kolumnach nie zgadzają się z wierszami")
        return [hr, hc]

