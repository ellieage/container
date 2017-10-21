import scrapy
import sys
import datetime
import subprocess

class ScrapeContainers:
    def __init__(self):
        subprocess.run(["rm",'container.json'])
        subprocess.run(["scrapy", "crawl", 'container', "-o", 'container.json'])
        print('Container Store storage section data updated on',datetime.date.today())
