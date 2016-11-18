import urllib, urllib2
import json


def detecterPFAM(infoProt, seqProt):
    #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    parameters = {
        'hmmdb':'pfam',
        'seq':'>' + infoProt + '\n' + seqProt + '\n'
    }
    enc_params = urllib.urlencode(parameters);


    request = urllib2.Request('http://www.ebi.ac.uk/Tools/hmmer/search/hmmscan',enc_params)

    #get the url where the results can be fetched from
    results_url = urllib2.urlopen(request).geturl()#.getheader('location')

    print(results_url)

    # modify the range, format and presence of alignments in your results here
    res_params = {
        'output':'json',
        'range':'1,10'
    }

    # add the parameters to your request for the results
    enc_res_params = urllib.urlencode(res_params)
    modified_res_url = results_url + '?' + enc_res_params

    # send a GET request to the server
    results_request = urllib2.Request(modified_res_url)
    data = urllib2.urlopen(results_request)

    donnees = data.read().decode('utf-8')


    j = json.loads(donnees)
    domaines = ""
    domainesReturn = []
    try:
        auxDoms = j['results']['hits']

        for dom in auxDoms:
            domaines = dom['acc'] + " " + domaines

        domainesReturn = speparerDomaines(domaines)

        print(domainesReturn)

    except IndexError:
        domainesReturn = ["--NA--"]
    return domainesReturn

def speparerDomaines(domainesPass):
    PFdom = []
    domainesVec = domainesPass.split(' ')
    domainesVec = domainesVec[:-1]
    if len(domainesVec) != 0:
        for dom in domainesVec:
            #print "DOM: " + dom
            PFdom.append(dom.split('.')[0])
    else:
        PFdom = ["--NA--"]
    return PFdom

if __name__ == '__main__':
    print(detecterPFAM('2abl_A mol:protein length:163  ABL TYROSINE KINASE', 'MGPSENDPNLFVALYDFVASGDNTLSITKGEKLRVLGYNHNGEWCEAQTKNGQGWVPSNYITPVNSLEKHSWYHGPVSRNAAEYLLSSGINGSFLVRESESSPGQRSISLRYEGRVYHYRINTASDGKLYVSSESRFNTLAELVHHHSTVADGLITTLHYPAP'))