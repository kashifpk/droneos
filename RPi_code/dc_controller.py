import RPi.GPIO as G

G.cleanup()
G.setmode(G.BOARD)


G.setup(7, G.OUT)
G.setup(11, G.OUT)
G.setup(13, G.OUT)
G.setup(15, G.OUT)

ch = ''

while True:
    ch = raw_input("Enter action [pin signal] or 'q' to quit: ")
    ch = ch.strip()
    
    if 'q' == ch:
        break
    else:
        pin, sig = ch.split(' ')
        G.output(int(pin), int(sig))
