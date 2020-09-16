import os
import praw
import pdb
import sys
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import subprocess

#return here to add setup input for praw.ini file
reddit = praw.Reddit('bot1')

#checks for and opens subscribers.txt, creates it if not present at Chirper filepath
if not os.path.isfile("subscribers.txt"):
    subscribers = []
    open("subscribers.txt", "w+")
else:
    with open("subscribers.txt", "r") as f:
        subscribers = f.read()
        subscribers = subscribers.split('\n')
        subscribers = list(filter(None, subscribers))
        
#checks for and opens  sub.txt, creates it if not there and assigns variable 'sub'
if not os.path.isfile('sub.txt'):
    subreddit = []
    f = open('sub.txt', 'w+')
if os.path.isfile('sub.txt'):
    with open('sub.txt', 'r') as f:
        sub = f.read()
               
#main App
class chirper:
    
    #tkinter master loop
    def __init__(self, master):
        
        #tkinter master 
        frame = Frame(master)
        frame.pack()
        root.title("Reddit Chirper")
        self.button = Button(frame, text='Exit', fg='red', command=root.destroy)
        self.button.grid(row=1, column=2)
        
        self.scan = Button(frame, text='Scan for new subscriptions', fg='black', command=self.scan)
        self.scan.grid(row=0, column=0)
        
        self.assign_sub = Button(frame, text='Assign a new subreddit', fg='black', command=self.assign_sub)
        self.assign_sub.grid(row=0, column=2)
        
        self.scan2 = Button(frame, text='Scan for unsubscriptions', fg='black', command=self.scan2)
        self.scan2.grid(row=0, column=1)
        
        self.print_subs = Button(frame, text='Print subscribers in Python console', fg='black', command=self.print_subs)
        self.print_subs.grid(row=1, column=1)
        
    #scans for new subscribers in assigned subreddit
    def scan(self):
        subreddit = reddit.subreddit(sub)
        for comment in subreddit.stream.comments():
            if comment.author.name not in subscribers and re.search('chirperadd!', comment.body, re.IGNORECASE):
                comment.reply("You have been subscribed. You will receive an update whenever the author posts a new story in their subreddit. Comment 'chirperremove!' to unsubscribe.")
                print(comment.author.name + ' subscribed!')
                subscribers.append(comment.author.name, '\n')
                
            elif comment.author.name in subscribers and re.search("chirperadd!", comment.body, re.IGNORECASE):
                                    print('No new subscribers.')
                                    break
            
    #scans for unsubscriptions in assigned subreddit (unfinished)
    def scan2(self):
        subreddit = reddit.subreddit(sub)
        for comment in subreddit.stream.comments():
            if comment.author.name in subscribers and re.search("chirperremove!", comment.body, re.IGNORECASE):
                comment.reply("You have been unsubscribed.")
                print(comment.author.name + ' unsubscribed.')


    #code to assign subreddit scope
    def assign_sub(self):
        subreddit = []
        f = open('sub.txt', 'w+')
        root.withdraw()
        sub = simpledialog.askstring(title='Subreddit Assignment',
                                     prompt='Set a subreddit to scan:')
        if sub == None:
            root.deiconify()           
        elif sub != None:
            f.write(sub)
            print('New sub',"'", sub, "'", 'assigned successfully')  
            root.deiconify()                    
                
    #placeholder, prints subscribers in console
    def print_subs(self):
        print(subscribers)
            

root=Tk()
app = chirper(root)

root.mainloop()
        


