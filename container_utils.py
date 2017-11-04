import json
from pprint import pprint
from fractions import Fraction
from collections import Counter
import os
import sys

class Container:


    def __init__(self, json_file_name='container.json'):

        """
        Loads container.json and stores as global(?) variable 'data'

        'data' is a list of dictionaries.
            Each dictionary contains the 'title' (name) of the container, its 'url',
            a list of the 'dimensions' available, a list of the 'price'(s) in the same order as dimension,
            and a link to the url of the 'image'.
                (Do not have the image working yet, price not working for some of the items
                    - the ones that have only 2 dimensions(?))

        Raises:
            throws exception if the file is not there.(KeyError? IOEXception?)
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

    def create_category(self):
        """
        Stores the category ('Decorative Bins and Baskets', 'Plastic Bins and Baskets', etc)
            for each item (dictionary) in the list 'data'.
            'category' becomes a new key for each dictionary in 'data'
        Also stores a Counter() called 'c' that counts the number of items in 'data' that are in each category:
            so 'c' is a dictionary with keys the categories, and value the number of titles that have this category.

        Raises:
            Should we raise something if the category isn't found?
                Not a problem yet becuase of the way containerstore is organized.

        """
        for d in self.data:
            category = d['url'].split('/')[5]
            d['category']=category
        self.c = Counter()
        for d in self.data:
            self.c[d['category']] += 1


    def create_new_dimensions(self):
        """
        Runs through the 'dimensions' of each dictionary in 'data'.
            Stores a new key 'new dimensions' that records the dimensions as a list of floats (in inches)

        Raises:
            Should we raise something if the dimensions aren't found?  Right now leaves as empty list.

        """


        # loop through the container links
        for j in range (0,len(self.data)):
            self.data[j]['new dimensions']=[]
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

    def organize_new_dimensions(self):

        """
        Creates a new variable 'dimensions' that is a list of lists of dictionaries.
            dictionaries with 3 dimensions found are all together in the third spot of the list.
                (I was doing this for the 'perfect fit' function.  I wanted to look through the dictionaries
                with 2 dimensions in a different way than those with 3 dimensions, and 1 or 2 dimensions only
                in emergency.  I am concered that storing everything may be unnecessary and take up too much
                storage if the data set is really big.)

        """

        self.dimensions = [[],[],[],[]] #stores zero, one, two, three dimensions

        for j in range(0,len(self.data)):
            if((self.data[j]['new dimensions'])==[]):
                self.dimensions[0].append([self.data[j],0])
            num_of_containers  = len(self.data[j]['new dimensions'])
            for k in range(0,num_of_containers):
                num_dim = len(self.data[j]['new dimensions'][k])


                #save the container and the spot that has these particular dimensions
                self.dimensions[num_dim].append([self.data[j],k])





    #  The the_perfect_fit function will be given 6 values, 2 for each dimension (a lower and upper limit).
    #  It returns the possible containers.


    def the_perfect_fit_ranges(self,ranges):

        """
        Searches for cantiners that fit in a given range of dimensions, using the 'dimensions' variable,
            created in 'organize_new_dimensions' function (a list of lists of dictionaries containing
            container information).
        Based on whether 0,1,2, or 3 dimensions are given, a different strategy is used.

        Args:
            ranges: a list of 6 floats, two for each dimension, providing the lower and upper bound.
                for example to find a container in the range 6-8.25" x 9-12" x 5-7", the variable would be
                ranges = [6.,8.25,9.,12.,5.,7.]
        Returns:
            possibles: a list of 4 lists of dictionaries of containers that might work.
                The 4 lists correspond to containers with 0,1,2, or 3 dimensions found.
        """

        if len(ranges)==6:

            possibles = [[],[],[],[]]

            possibles[0]=self.dimensions[0]

            for d in self.dimensions[1]:
                if ((ranges[0]<d[0]['new dimensions'][d[1]][0]<ranges[1])
                    or (ranges[2]<d[0]['new dimensions'][d[1]][0]<ranges[3])
                    or (ranges[4]<d[0]['new dimensions'][d[1]][0]<ranges[5])):

                    possibles[1].append(d)

            for d in self.dimensions[2]:
                if ( (ranges[0] < d[0]['new dimensions'][d[1]][0] < ranges[1])  and (ranges[2] < d[0]['new dimensions'][d[1]][1] < ranges[3]) ):

                    possibles[2].append(d)

            for d in self.dimensions[3]:
                if ((ranges[0]<d[0]['new dimensions'][d[1]][0]<ranges[1]) and (ranges[2]<d[0]['new dimensions'][d[1]][1]<ranges[3])
                    and (ranges[4]<d[0]['new dimensions'][d[1]][2]<ranges[5])):

                    possibles[3].append(d)


            return possibles


    def the_perfect_fit_values(self,values,diffmax=2.):

        """
        Searches for continers that are closest to the given 3 dimensions, using the 'dimensions' variable,
            created in 'organize_new_dimensions' function (a list of lists of dictionaries containing
            container information).
        Based on whether 0,1,2, or 3 dimensions are given, a different strategy is used.
        Currently only looking at containers with 3 dimensions given:
            looks for boxes with each dimension within .5", then 1", so on until the given upper bound.

        Args:
            values: a list of 3 floats, one for each dimension
            diffmax: an upper bound on the error of the dimensions
        Returns:
            possibles: a list of 4 lists of dictionaries of containers that might work.
                The 4 lists correspond to containers with 0,1,2, or 3 dimensions found.
        """

        if len(values)==3:

            possibles = [[],[],[],[]]

            possibles[0]=self.dimensions[0]

            diff = 0.5


            while diff<=diffmax:
                for d in self.dimensions[3]:

                    if ((abs(values[0]-d[0]['new dimensions'][d[1]][0])<=diff) and (abs(values[1]-d[0]['new dimensions'][d[1]][1])<=diff)
                    and (abs(values[2]-d[0]['new dimensions'][d[1]][2])<=diff)):

                        if (d not in possibles[3]):

                            possibles[3].append(d)

                diff+=.5

            return possibles
