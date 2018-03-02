import statistics


# Checks if value is a date; False if:  empty, malformed
def is_date(s):
    try:
        int(s)
        return (len(str(s))==8)
    except ValueError:
        pass

    return False

# Checks if value is a zip code; False if: empty, fewer than five digits
def is_zip(s):
    try:
        int(s)
        return (len(str(s))>=5)
    except ValueError:
        pass

    return False

"""
class Insight:

Reads in political campaign contribution file, itcont.txt, from the Federal Election Commission, outputs two files, medianvals_by_zip.txt and medianvals_by_date.txt

Args:
    file_input: name of input file, defaults to 'example1/itcont.txt'
        if no string is given
    file_zip_output: name of output file to store zip code data,
        defaults to "example1/medianvals_by_zip.txt" if no string is given
    file_date_output: name of output file to store date data,
        defaults to "example1/medianvals_by_date.txt" if no string is given
"""
class Insight:
    def __init__(self, file_input = 'example1/itcont.txt',
file_zip_output = "example1/medianvals_by_zip.txt",
file_date_output = "example1/medianvals_by_date.txt"):
        medianvals_by_zip = open(file_zip_output,"w+")
        medianvals_by_date = open(file_date_output,"w+")

        # large dictionary to keep track of the zip code information,
        # keys: (CMTE_ID,ZIP_CODE), value: list of TRANSACTION_AMT values
        master_d_zip = {}

        # large dictionary to keep track of the date information,
        # keys: (CMTE_ID,TRANSACTION_DT), value: list of TRANSACTION_AMT values
        master_d_date = {}

        # open the given file; the political campaign contribution file, itcont.txt

        with open(file_input) as f:
            # read file line by line
            for line in f:

                # save a list of the details in the line
                mylist = line.split('|')
                # make sure the list is the expected size
                if (len(mylist)==21):
                    # store the information in the line as a dictionary, keeping only the information we need
                    d = {'CMTE_ID' : mylist[0], 'ZIP_CODE' : mylist[10][:5] # zip: first 5 digits only
                        ,'TRANSACTION_DT' : mylist[13], 'TRANSACTION_AMT' : mylist[14], 'OTHER_ID' : mylist[15]}

                    # OTHER_ID must be empty
                    # CMTE_ID and TRANSACTION_AMT must be Nonempty
                    if (d['CMTE_ID']!='' and d['TRANSACTION_AMT']!='' and d['OTHER_ID']==''):

                        # zip - write as you read in
                        # must have a valid Zip
                        if (is_zip(d['ZIP_CODE'])==True):

                            # if the key (CMTE_ID,ZIP_CODE) already exists, add the TRANSACTION_AMT to the list
                            # otherwise create the key and start a list with the TRANSACTION_AMT as the first entry
                            master_d_zip.setdefault((d['CMTE_ID'],d['ZIP_CODE']), []).append(int(d['TRANSACTION_AMT']))

                            # write to the zip file:
                            # "CMTE_ID|ZIP_CODE|median transaction|number of transactions|total transactions"
                            medianvals_by_zip.write(''+d['CMTE_ID']+'|'+d['ZIP_CODE']+'|'+ str(round(statistics.median(master_d_zip[(d['CMTE_ID'],d['ZIP_CODE'])])))+ '|'
                                                    +str(len(master_d_zip[(d['CMTE_ID'],d['ZIP_CODE'])]))+'|'
                                                    +str(sum(master_d_zip[(d['CMTE_ID'],d['ZIP_CODE'])]))+'\n')

                        # date - wait to write
                        # must have a valid date
                        if (is_date(d['TRANSACTION_DT'])==True):

                            # if the key (CMTE_ID,TRANSACTION_DT) already exists, add the TRANSACTION_AMT to the list
                            # otherwise create the key and start a list with the TRANSACTION_AMT as the first entry
                            master_d_date.setdefault((d['CMTE_ID'],d['TRANSACTION_DT']), []).append(int(d['TRANSACTION_AMT']))

        # write date file
        # start by sorting the dictionary by the key (CMTE_ID,TRANSACTION_DT)
        for d in sorted(master_d_date):

            # write to the date file:
            # "CMTE_ID|TRANSACTION_DT|median transaction|number of transactions|total transactions"
            medianvals_by_date.write(''+d[0]+'|'+d[1]+'|'+str(round(statistics.median(master_d_date[d]))) + '|'
                                     + str(len(master_d_date[d]))+'|'
                                     + str(sum(master_d_date[d]))+'\n')
