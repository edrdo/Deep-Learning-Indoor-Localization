#! /usr/bin/python3
from Common import Model

if __name__ == '__main__':
    import os
    import sys
    import getopt

    model_id = 'tomas'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'm:p:r:c:')
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    max_results = 5
    min_confidence = None
    path = os.path.join(os.path.dirname(sys.argv[0]),'models')
    for o, a in opts: 
        if o == '-m':
            model_id = a
        elif o == '-p':
            path = a
        elif o == '-n':
            max_results = a
        elif o == 'c':
            min_confidence = a
    model = Model(os.path.join(path,model_id))

    for file in args:
        print(file)
        results = model.classify(file, max_results, min_confidence)
        for i,r in enumerate(results):
            print('{},{},{},{:.2f}'.format(file, i+1, r[0], r[1]))

