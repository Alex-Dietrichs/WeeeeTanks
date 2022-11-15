from cmu_112_graphics import *

def appStarted(app): 
    app.messages = ['appStarted']

def appStopped(app):
    app.messages.append('appStopped')
    print('appStopped!')

def keyPressed(app, event):
    app.messages.append('keyPressed: ' + event.key)

def keyReleased(app, event):
    app.messages.append('keyReleased: ' + event.key)

def mousePressed(app, event):
    app.messages.append(f'mousePressed at {(event.x, event.y)}')

def mouseReleased(app, event):
    app.messages.append(f'mouseReleased at {(event.x, event.y)}')

def mouseMoved(app, event):
    app.messages.append(f'mouseMoved at {(event.x, event.y)}')

def mouseDragged(app, event):
    app.messages.append(f'mouseDragged at {(event.x, event.y)}')

def sizeChanged(app):
    app.messages.append(f'sizeChanged to {(app.width, app.height)}')

def redrawAll(app, canvas):
    font = 'Arial 20 bold'
    canvas.create_text(app.width/2,  30, text='Events Demo',
                       font=font, fill='black')
    n = min(10, len(app.messages))
    i0 = len(app.messages)-n
    for i in range(i0, len(app.messages)):
        canvas.create_text(app.width/2, 100+50*(i-i0),
                           text=f'#{i}: {app.messages[i]}',
                           font=font, fill='black')

runApp(width=600, height=600)