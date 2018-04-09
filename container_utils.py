import json
from pprint import pprint
from fractions import Fraction
import unicodedata
from collections import Counter
import os
import sys



class ContainerClean_conStore:
    """
        Loads the file: containerRaw_conStore.json (scraped from the Container Store website)
        Stores this json as self.data, a list of dictionaries (a dictionary for each type of container)
        Cleans the dimensions from strings to a list of floats, [length, width, height]
            (stored with key: "new dimensions")
        Writes self.data to containerClean_conStore.json
    """


    def __init__(self, json_file_name='containerRaw_conStore.json'):
        """
        Loads containerRaw_conStore.json and stores as variable 'data'

        'data' is a list of dictionaries, one for each type of container.

        Each type of container has one url, title, and image (for now), but may have multiple sizes, so the dimensions and price are both lists.  The image is also stored as a list, but we have found that it is best to store just one image per 'type'.
                Format of containerRaw_conStore.json:
                    [{"url":"https:...",
                    "title": "Container Name",
                    "dimensions": [' length" x width " x height " ', ' length" x width " x height " ',...],
                    "price": ['price1','price2',...],
                    "image": ["https:..."]},...]

        Raises:
            throws exception if the file is not there.
        """

        if os.path.exists(json_file_name):
            with open(json_file_name) as data_file:
                try:
                     self.data = json.load(data_file)
                except ValueError:
                    print("File '{}' is empty.".format(json_file_name), file=sys.stderr)
                    self.data = []

            # with open('container.json', 'r') as f:
            #     self.data = json.load(f)
        else:
            print("No such file '{}'".format(json_file_name), file=sys.stderr)
            self.data = []
        # Remove duplicates

        # self.data = [i for n, i in enumerate(self.data) if i not in self.data[n + 1:]]



    def create_category(self):
        """
        Stores the category ('Decorative Bins and Baskets', 'Plastic Bins and Baskets', etc)
            for each item (dictionary) in the list 'data'.
            'category' becomes a new key for each dictionary in 'data'
        Also stores a Counter() called 'c' that counts the number of items in 'data' that are in each category:
            so 'c' is a dictionary with keys the categories, and value the number of titles that have this category.

        Raises:
            Should we raise something if the category isn't found?
                Not a problem yet becuase of the way Container Store is organized.

        """
        for d in self.data:
            category = d['url'].split('/')[5]
            d['category']=category
        self.c = Counter()
        for d in self.data:
            self.c[d['category']] += 1

    def create_new_dimensions(self):
        """
        Cleans the 'dimensions' of each dictionary in 'data' by storing a new key, 'new dimensions' for each dictionary in 'data' with the cleaned up dimensions (lists of floats)

        The value corresponding to the 'dimensions' key in the dictionaries of data are list of strings that typically look like:
        "dimensions": [' length" x width " x height " ', ' length" x width " x height " ',...],
        Real examples:
        'dimensions': ["6-1/4\" x 11\" x 5-1/8\" h", "7-3/4\" x 13\" x 5-3/4\" h"]
            or
        'dimensions': ["\n                            ", "\n                            ", "\n                            ", "\n                        ", "\n                            ", "\n                            ", "\n                            ", "\n                        ", "\n                                ", "\n                                ", "\n                                ", "\n                            ", "\n                                ", "\n                                ", "\n                                ", "\n                            ", "18\" x 21\" x 41\" h"]
            or
        'dimensions':["22\" diam. x 8\" h"]

        New key in 'data' is 'new dimensions' with the structure:
        'new dimensions': [[l,w,h],[l,w,h],...]
            (where the l's, w's, and h's are floats representing inches)
        Real examples:
        'dimensions': [[6.25, 11.0, 5.125], [7.75, 13, 5.75]]
            or
        'dimensions': [[18.0, 21.0, 41.0]]
            or
        'dimensions':[[22.0, 22.0, 8.0]]
            Some dimensions are empty or only one or two dimensions are found -
                this is handled later in the Container_Organize class
        """


        # loop through the container links
        for j in range (0,len(self.data)):
            self.data[j]['new dimensions']=[]
            self.data[j]['dimensions text']=self.data[j]['dimensions']
            # many container links have containers available in several different sizes, so we roam through each one
            for k in range(0,len(self.data[j]['dimensions'])):
                dim_no_whitespace = self.data[j]['dimensions'][k].strip()
                if (dim_no_whitespace != ""):
                    mydim = self.data[j]['dimensions'][k].split('x')
                    newdim = []
                    # each dimension of the container needs to be converted to a float and added to 'new dimensions'
                    for i in range (0,len(mydim)):

                        mysplit = mydim[i].split('sq.')[0]
                        if '-' in mysplit:
                            this_split = mysplit.split('-')
                            num =0
                            for p in this_split:
                                num += float(Fraction(p.split('"')[0]))
                        else:
                            # dimensions in feet:
                            if("'" in mysplit):
                                num = int(mysplit.split("'")[0])*12

                            else:
                                num = float(Fraction(mysplit.split('"')[0]))

                        # if the entry notes that it is square or a diameter, then the dimension needs to be inserted in two spots
                        double=int(('sq.' in mydim[i]) or ('diam.' in mydim[i]))
                        for _ in range(0,double+1):
                            newdim.append(num)
                    self.data[j]['new dimensions'].append(newdim)

    def write_file(self):
        """
        The write_file function writes self.data to containerClean_conStore.json
        """

        with open('containerClean_conStore.json', 'w') as outfile:
            json.dump(self.data, outfile)
        print('containerClean_conStore.json written.')


def convertImproperFractions(improperFraction):

    if (len(improperFraction) == 1):
        return unicodedata.numeric(improperFraction)

    if (len(improperFraction) > 1) & (not (improperFraction[:len(improperFraction)-1].isdigit())):
        raise ArithmeticError("The format needs to be numbers ending with a improper fraction. The number inserted was " +
                              str(improperFraction))

    if improperFraction[len(improperFraction)-1].isdigit():
        return float(improperFraction)
    else:
        return float(improperFraction[:len(improperFraction)-1]) + unicodedata.numeric(improperFraction[len(improperFraction)-1])


class ContainerClean_ikea:
    """
    The "ContainerClean_ikea" class:
        Loads the file: containerRaw_conStore.json (scraped from the Ikea website)
        Stores this json as self.data, a list of dictionaries (a dictionary for each type of container)
        Cleans the dimensions from strings to a list of floats, [length, width, height] (in inches)
            (stored with key: "new dimensions")
        Writes self.data to containerClean_ikea.json
    """

    def __init__(self, json_file_name='containerRaw_ikea.json'):

        """
        Loads containerRaw_ikea.json and stores as variable 'data'

        'data' is a list of dictionaries, one for each type of container.

        Each type of container has one url, title, and image (for now), but may have multiple sizes, so the dimensions and price are both lists.  The image is also stored as a list, but we have found that it is best to store just one image per 'type'.
        Format of containerRaw_conStore.json:
            [{"url":"https:...",
            "title": "Container Name",
            "dimensions": [' length" x width " x height " ', ' length" x width " x height " ',...],
            "price": ['price1','price2',...],
            "image": ["https:..."]},...]

        Raises:
            throws exception if the file is not there.
        """

        if os.path.exists(json_file_name):
            with open(json_file_name) as data_file:
                try:
                     self.data = json.load(data_file)
                except ValueError:
                    print("File '{}' is empty.".format(json_file_name), file=sys.stderr)
                    self.data = []

        else:
            print("No such file '{}'".format(json_file_name), file=sys.stderr)
            self.data = []

    def create_new_dimensions(self):

        dim_strings=['Length','Width','Height','Depth']

        for j in range(0,len(self.data)):
            self.data[j]['new dimensions']=[]
            self.data[j]['dimensions text'] = []
            if any(s in k for k in self.data[j]['dimensions'] for s in dim_strings):
                newdim = []
                newtext = ''
                for i in range(0,len(self.data[j]['dimensions'])):

                    dim_no_whitespace = self.data[j]['dimensions'][i].strip()
                    # print(dim_no_whitespace)
                    # newtext.append(dim_no_whitespace)
                    if any(s in dim_no_whitespace for s in dim_strings):

                        text = dim_no_whitespace.split(':')[1]
                        if newtext != '':
                            newtext+=' x '
                        newtext+=text
                        whole_frac = dim_no_whitespace.split(':')[1].split()

                        whole = float(whole_frac[0])
                        if (len(whole_frac)==3):
                            frac=0.
                            s=whole_frac[1]
                            try:
                                unicodedata.numeric(s)
                                frac=unicodedata.numeric(s)
                            except (TypeError, ValueError):
                                pass
                            try:
                                Fraction(s)
                                frac=float(Fraction(s))
                            except (TypeError, ValueError):
                                pass
                            newdim.append(whole+frac)
                        elif (len(whole_frac)==2):
                            newdim.append(whole)
                self.data[j]['dimensions text'].append(newtext)
                self.data[j]['new dimensions'].append(newdim)
            else:
                for i in range(0,len(self.data[j]['dimensions'])):
                    newdim = []
                    for mydim in self.data[j]['dimensions'][i].strip().split('x'):
                        newstr = mydim.replace('"', '').replace('.','').replace('(','').replace(')','').replace(',','')
                        number = convertImproperFractions(newstr)
                        newdim.append(number)
                    self.data[j]['new dimensions'].append(newdim)

    def write_file(self):
        """
        The write_file function writes self.data to containerClean_ikea.json
        """

        with open('containerClean_ikea.json', 'w') as outfile:
            json.dump(self.data, outfile)
        print('containerClean_ikea.json written.')






class Container_Aggregate:
    def __init__(self, json_conStore='containerClean_conStore.json', json_ikea='containerClean_ikea.json', json_amazon='container_amazon.json'):

        """
        Loads containerClean_conStore.json and stores as variable 'data_conStore'
        Loads containerClean_ikea.json and stores as variable 'data_ikea'

        Raises:
            throws exception if the file is not there.
        """

        if os.path.exists(json_conStore):
            with open(json_conStore) as data_conStore:
                try:
                     self.data_conStore = json.load(data_conStore)
                except ValueError:
                    print("File '{}' is empty.".format(json_conStore), file=sys.stderr)
                    self.data_conStore = []

            # with open('container.json', 'r') as f:
            #     self.data = json.load(f)
        else:
            print("No such file '{}'".format(json_conStore), file=sys.stderr)
            self.data_conStore = []

        if os.path.exists(json_ikea):
            with open(json_ikea) as data_ikea:
                try:
                     self.data_ikea = json.load(data_ikea)
                except ValueError:
                    print("File '{}' is empty.".format(json_ikea), file=sys.stderr)
                    self.data_ikea = []

        else:
            print("No such file '{}'".format(json_ikea), file=sys.stderr)
            self.data_ikea = []

        if os.path.exists(json_amazon):
            with open(json_amazon) as data_amazon:
                try:
                     self.data_amazon = json.load(data_amazon)
                except ValueError:
                    print("File '{}' is empty.".format(json_amazon), file=sys.stderr)
                    self.data_amazon = []

        else:
            print("No such file '{}'".format(json_ikea), file=sys.stderr)
            self.data_ikea = []

        with open('container_agg.json', 'w') as outfile:

            json.dump(self.data_conStore + self.data_ikea+ self.data_amazon, outfile)

        print('container_agg.json written')





class Container_Organize:
    def __init__(self, json_file_name='container_agg.json'):

        """
        Loads container_agg.json and stores as variable 'data'

        Raises:
            throws exception if the file is not there.
        """

        if os.path.exists(json_file_name):
            with open(json_file_name) as data_file_name:
                try:
                     self.data = json.load(data_file_name)
                except ValueError:
                    print("File '{}' is empty.".format(json_file_name), file=sys.stderr)
                    self.data = []


        else:
            print("No such file '{}'".format(json_file_name), file=sys.stderr)
            self.data = []


    def organize_new_dimensions(self):

        """
        Creates a new variable 'dimensions' that is a list of dictionary, place in the list of dimensions/prices
            dictionaries with 3 dimensions found are all together in the third spot of the list.
                (I was doing this for the 'perfect fit' function.  I wanted to look through the dictionaries
                with 2 dimensions in a different way than those with 3 dimensions, and 1 or 2 dimensions only
                in emergency.  I am concered that storing everything may be unnecessary and take up too much
                storage if the data set is really big.)


        """

        self.dimensions = [[],[],[],[],[],[]] #stores zero, one, two, three, four dimensions

        for j in range(0,len(self.data)):
            if((self.data[j]['new dimensions'])==[]):
                self.dimensions[0].append([self.data[j],0])
            num_of_containers  = len(self.data[j]['new dimensions'])
            for k in range(0,num_of_containers):
                num_dim = len(self.data[j]['new dimensions'][k])

                # print(num_dim,j,k)
                #save the container and the spot that has these particular dimensions

                self.dimensions[num_dim].append([self.data[j],k])

    def write_file(self):
        """
        The write_file function writes self.data to containerClean_ikea.json
        """

        with open('container_org.json', 'w') as outfile:
            json.dump(self.dimensions, outfile)
        print('container_org.json written.')
