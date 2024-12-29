from time import sleep
def loadingMotion():
    symbols = '[' + ' ' * 100 + ']'
    start = 1
    stop = len(symbols) - 1
    for num in range(start, stop):
        if num == stop - 1:
            sleep(.02)
            symbols = symbols[0:num] + '>]'
            print(symbols, end='\r')
            sleep(1)
            break
        sleep(.02)
        symbols = symbols[0:num] + '=' + symbols[num + 1:] 
        print(symbols, end='\r')

