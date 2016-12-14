

def chunks(tab, n):
    return [tab[x:x+n] for x in range(0, len(tab), n)]

data = [0,1,2,3,4,5,6,7,8,9]

print(list(chunks(data, 4)))

