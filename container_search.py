import json
# from pprint import pprint
# from fractions import Fraction
# from collections import Counter
import os
# import sys
from pprint import pprint

class ContainerSearch:
    # def __init__(self, data, c, dimensions):
    # def __init__(self, data, c, dimensions):
    # def __init__(self, json_file_name='data_cleaned.json', c_file_name='data_c.json', dim_file_name='data_dim.json'):
    def __init__(self, json_file_name='container_agg.json', dim_file_name='container_org.json'):
        """
        This class is to be used by the website
        Everything else can be tidied up in the background

        Loads data_cleaned.json and stores as class variable 'data'

        'data' is a list of dictionaries.
            Each dictionary contains the 'title' (name) of the container, its 'url',
            a list of the 'dimensions' available, a list of the 'price'(s) in the same order as dimension,
            and a link to the url of the 'image'.
            Also a list of 'new dimensions' and category, calculated in container_utils.py

        Raises:
            throws exception if the file is not there.(KeyError? IOEXception?)
        """

        if os.path.exists(json_file_name):
            with open(json_file_name) as data_file:
                try:
                     self.data = json.load(data_file)
                except ValueError:
                    print("File '{}' is empty.".format(json_file_name))
                    self.data = []
        else:
            print("No such file '{}'".format(json_file_name))
            self.data = []
        #
        # if os.path.exists(c_file_name):
        #     with open(c_file_name) as data_file:
        #         try:
        #              self.c = json.load(data_file)
        #         except ValueError:
        #             print("File '{}' is empty.".format(c_file_name))
        #             self.c = []
        # else:
        #     print("No such file '{}'".format(c_file_name))
        #     self.c = []

        if os.path.exists(dim_file_name):
            with open(dim_file_name) as data_file:
                try:
                     self.dimensions = json.load(data_file)
                except ValueError:
                    print("File '{}' is empty.".format(dim_file_name))
                    self.dimensions = []
        else:
            print("No such file '{}'".format(dim_file_name))
            self.dimensions = []


    def the_perfect_fit_ranges(self,ranges):

        """
        Searches for continers that fit in a given range of dimensions, using the 'dimensions' variable,
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
            pf: a list of 5 lists of dictionaries of containers that might work.
                The 5 lists correspond to containers with 0,1,2, or 3, or 4 dimensions found.
        """

        if len(values)==3:

            pf = [[],[],[],[],[]]

            pf[0]=self.dimensions[0]

            diff = 0.1

            # d[0] = dictionary
            # d[1] = place in the list of dimensions/prices

            while (diff<=diffmax or len(pf[3])<10):
                temp = []
                for d in self.dimensions[3]:
                    e1 = abs(values[0]-d[0]['new dimensions'][d[1]][0])
                    e2 = abs(values[1]-d[0]['new dimensions'][d[1]][1])
                    e3 = abs(values[2]-d[0]['new dimensions'][d[1]][2])
                    error = e1+e2+e3

                    if ((e1 <= diff) and (e2 <= diff)
                    and (e3 <= diff)):
                        # pprint(d)
                        # print (d not in pf[3])
                        if (d not in pf[3]):

                            temp.append((d,error))

                        # if (d not in pf[3]):
                        #
                        #     pf[3].append(d)

                temp.sort(key=lambda x: x[1])
                # print('\n')
                # print(diff)
                # pprint(temp)

                for t in temp:
                    pf[3].append(t[0])

                diff+=.1

            return [pf,diff]
