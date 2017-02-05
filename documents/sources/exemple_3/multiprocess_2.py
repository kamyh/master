from multiprocessing import Pool

def f(x, y):
    return x+y

if __name__ == '__main__':
    p = Pool(processes=5)
    print(p.starmap(f, [[1,2],[3,4],[5,6]]))