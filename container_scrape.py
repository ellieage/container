import scrapy
import sys
import datetime
import subprocess

# Runs the spider for the Container Store, updates: containersRaw_conStore.json
# File has format:
class ContainerScrape_conStore:
    def __init__(self):

        # subprocess.run(["rm",'containerRaw_conStore.json'])
        subprocess.run(["scrapy", "crawl", 'container', "-o", 'containerRaw_conStore.json'])
        print('Container Store storage section data updated on',datetime.date.today())

# Runs the spider for the Ikea containers, updates: containersRaw_ikea.json
class ContainerScrape_ikea:
    def __init__(self):

        # subprocess.run(["rm",'containerRaw_ikea.json'])
        subprocess.run(["scrapy", "crawl", 'container_ikea', "-o", 'containerRaw_ikea.json'])
        print('IKEA storage section data updated on',datetime.date.today())
