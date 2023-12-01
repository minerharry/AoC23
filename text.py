
def getInput(file='input.txt'):
    with open(file,'r') as f:
        result = [t.strip('\n') for t in f.readlines()];
    return result
