# myscript.py
import os

region = os.getenv("REGION")
print(region) # will print "eu-central-1"

bucket = os.getenv("BUCKET")
print(bucket)