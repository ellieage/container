

class Container_Aggregate:
    def __init__(self, json_file_name='container.json'):

        """
        Loads container.json and stores as variable 'data'

        'data' is a list of dictionaries.
            Each dictionary contains the 'title' (name) of the container, its 'url',
            a list of the 'dimensions' available, a list of the 'price'(s) in the same order as dimension,
            and a link to the url of the 'image'.
                (Do not have the image working yet, price not working for some of the items
                    - the ones that have only 2 dimensions(?))

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


class Container_Organize:
    def __init__(self, json_file_name='container.json'):

        """
        Loads container.json and stores as variable 'data'

        'data' is a list of dictionaries.
            Each dictionary contains the 'title' (name) of the container, its 'url',
            a list of the 'dimensions' available, a list of the 'price'(s) in the same order as dimension,
            and a link to the url of the 'image'.
                (Do not have the image working yet, price not working for some of the items
                    - the ones that have only 2 dimensions(?))

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
