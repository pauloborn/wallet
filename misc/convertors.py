def money(n: str):
    if type(n) is not float:
        return float(n.replace('R$', '').replace('.', '').replace(',', '.').replace('%', ''))
    else:
        return n


def num(n: str):
    if n == 'NaN':
        return 0
    else:
        return int(n)
