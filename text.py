
def get_input(file='input.txt'):
    with open(file,'r') as f:
        result = f.read().splitlines()
    return result
