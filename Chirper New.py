import os
import sys
import subprocess
import praw
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import tkinter.scrolledtext as tkst
import tkinter as tk

#come back to add input for praw.ini file
reddit = praw.Reddit('bot1')
global commentids
if not os.path.isfile('commentids.txt'):
    commentids = []
    open('commentids.txt', 'w+')
    
with open('commentids.txt', 'r')as f:
    commentids = f.read()
    commentids = commentids.split('\n')
    commentids = list(filter(None, commentids))

if not os.path.isfile("subscribers.txt"):
    subscribers = []
    open("subscribers.txt", "w+")

with open("subscribers.txt", "r") as f:
    subscribers = f.read()
    subscribers = subscribers.split('\n')
    subscribers = list(filter(None, subscribers))
    printed_subs = str(subscribers)
    subscriber_number1 = len(subscribers)
    subscriber_number2 = str(subscriber_number1)
             
class chirper():
        
    def __init__(self, root):
        global sub
        if not os.path.isfile('sub.txt'):   
            f = open('sub.txt', 'w+')        
            root.withdraw()
            sub = simpledialog.askstring(title='Subreddit Assignment',
                                     prompt='Set a subreddit to scan:')
            if sub == None:
                root.deiconify()           
            elif sub != None:
                f.write(sub)
                print('New sub',"'", sub, "'", 'assigned successfully')
                global v
                v = StringVar()
                v.set('Scanning subreddit: ' + sub)
                root.deiconify()
        else:
            with open('sub.txt', 'r') as f:
                    sub = f.read()
                    v = StringVar()
                    v.set('Scanning subreddit: ' + sub)
            
        #tkinter master
        frame = Frame(root)
        frame.pack()
        root.title("Reddit Chirper")
        self.exit = Button(frame, text='Exit', fg='red', command=root.destroy)
        self.exit.grid(row=1, column=2)
            
        self.scan = Button(frame, text='Scan for new subscriptions and unsubscriptions', fg='black', command=self.scan)
        self.scan.grid(row=0, column=1)
        
        Label(root, textvariable=v).pack()
        
        self.assign_sub = Button(frame, text='Assign a new subreddit', fg='black', command=self.assign_sub)
        self.assign_sub.grid(row=0, column=2)
        
        self.send_message = Button(frame, text='Compose a message to your subscribers', fg='black', command=self.send_message)
        self.send_message.grid(row=1, column=1)
        
        textArea = tkst.ScrolledText()
        textArea.pack()
        textArea.insert(tk.INSERT,
                        subscriber_number2 + ' subscribers:  ' + printed_subs)
        
    #scans for new subscribers in assigned subreddit
    def scan(self):
        subreddit = reddit.subreddit(sub)
        for comment in reddit.subreddit(sub).comments():
            if comment.author.name not in subscribers and comment.id not in commentids and re.search("chirperadd!", comment.body, re.IGNORECASE):
                comment.reply('You have been subscribed.')
                print(comment.author.name + ' subscribed.')
                subscribers.append(comment.author.name)
                with open ("subscribers.txt", "w") as f:
                        for comment.author in subscribers:
                                f.write(comment.author.name + "\n")
                commentids.append(comment.id)      
                with open ('commentids.txt', 'w')as f:
                    for comment.id in commentids:
                        f.write(comment.id + '\n')
                         
            elif comment.author.name in subscribers and comment.id not in commentids and re.search("chirperremove!", comment.body, re.IGNORECASE):
                comment.reply("You have been unsubscribed.")
                print(comment.author.name + ' unsubscribed.')  
                commentids.append(comment.id)
                with open ('commentids.txt', 'w')as f:
                    for comment.id in commentids:
                        f.write(comment.id + '\n')
                subscribers.remove(comment.author.name) #removes the comment author from the subscribers list to update tkinter 'show subscribers' output
                with open ("subscribers.txt", "r+") as f:
                    lines = f.readlines()
                    f.seek(0)
                    for line in lines:
                        if line == comment.author.name:
                            f.write("")                
     
    def assign_sub(self):
        f = open('sub.txt', 'w+')
        root.withdraw()
        sub = simpledialog.askstring(title='Subreddit Assignment',
                                     prompt='Set a subreddit to scan:')
        if sub == None:
            root.deiconify()           
        elif sub != None:
            f.write(sub)
            print('New sub',"'", sub, "'", 'assigned successfully')
            v = StringVar()
            v.set('Scanning subreddit: ' + sub)
            root.update_idletasks()
            root.deiconify()
            
    global Hermes     
    def Hermes(self):
        print('placeholder function')
    
    def send_message(self):
        messenger = tk.Toplevel()
        messenger.title('Compose message')
        
        message_input = Text(messenger, bg='lightgrey')
        message_input.pack()
        
        self.send = Button(messenger, text='Send message', fg='black', command=lambda: [messenger.destroy(), Hermes(self)])
        self.send.pack()
    
if __name__ == '__main__':
    root=tk.Tk()
    chirper(root)
    root.mainloop()
