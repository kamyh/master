from hmmerScan import HmmerScan


def test_10102016():
    h = HmmerScan()
    h.docker_ps()

def test_13102016():
    h = HmmerScan()
    h.compute_domaine_from_host()


if __name__ == '__main__':
    test_10102016()