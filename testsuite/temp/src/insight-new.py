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

def search(lst, target):
    min = 0
    max = len(lst)
    avg = int((min+max)/2)
#     print (lst, target, avg , (min,max))
    while (min < max):
        if (lst[avg] == target):
            return avg
        elif (lst[avg] < target):
#             print(lst[avg], ' < ', target, ' avg = ', avg, 'min, max : ', min, max)
            return avg + 1 + search(lst[avg+1:], target)
        else:
#             print(lst[avg], ' > ', target, ' avg = ', avg, 'min, max : ', min, max)
            return search(lst[:avg], target)

    return avg



class Insight2:
    def __init__(self, file_input = 'test_sorted/itcont.txt',
file_zip_output = "test_sorted/medianvals_by_zip.txt",
file_date_output = "test_sorted/medianvals_by_date.txt"):
        medianvals_by_zip = open(file_zip_output,"w+")
        medianvals_by_date = open(file_date_output,"w+")

        # perhaps use only one master_d in the future, use these ones to check
        master_d_zip = {}
        master_l_date = []
        d_date = {}

        with open(file_input) as f:
            for line in f:
                mylist = line.split('|')  # this is always? of length 21
                if (len(mylist)==21):
                    d = {'CMTE_ID' : mylist[0], 'ZIP_CODE' : mylist[10][:5] # zip: first 5 digits only
                        ,'TRANSACTION_DT' : mylist[13], 'TRANSACTION_AMT' : mylist[14], 'OTHER_ID' : mylist[15]}

                    if (d['CMTE_ID']!='' and d['TRANSACTION_AMT']!='' and d['OTHER_ID']==''):
                        # process this one (applies to both files)



                        # zip - write as you read in
                        if (is_zip(d['ZIP_CODE'])==True):
                            master_d_zip.setdefault((d['CMTE_ID'],d['ZIP_CODE']), []).append(int(d['TRANSACTION_AMT']))
                            medianvals_by_zip.write(''+d['CMTE_ID']+'|'+d['ZIP_CODE']+'|'+ str(round(statistics.median(master_d_zip[(d['CMTE_ID'],d['ZIP_CODE'])])))+ '|'
                                                    +str(len(master_d_zip[(d['CMTE_ID'],d['ZIP_CODE'])]))+'|'
                                                    +str(sum(master_d_zip[(d['CMTE_ID'],d['ZIP_CODE'])]))+'\n')

                        # date - wait to write
                        if (is_date(d['TRANSACTION_DT'])==True):

                            spot = search(master_l_date,(d['CMTE_ID'],d['TRANSACTION_DT']))
#                             print('search result: ', spot)

                            if spot==len(master_l_date):
                                master_l_date.append((d['CMTE_ID'],d['TRANSACTION_DT']))
                                d_date[(d['CMTE_ID'],d['TRANSACTION_DT'])]=[int(d['TRANSACTION_AMT'])]
#                                 print('add to end of list', master_l_date, d_date)

                            elif (master_l_date[spot] == (d['CMTE_ID'],d['TRANSACTION_DT'])):
                                d_date[(d['CMTE_ID'],d['TRANSACTION_DT'])].append(int(d['TRANSACTION_AMT']))
#                                 print ('Already in the list',(d['CMTE_ID'],d['TRANSACTION_DT']), '\n', d_date)
                            else:
                                master_l_date.insert(spot, (d['CMTE_ID'],d['TRANSACTION_DT']))
                                d_date[(d['CMTE_ID'],d['TRANSACTION_DT'])]=[int(d['TRANSACTION_AMT'])]
#                                 print('insert into list at position: ', spot)


        for i in range(0,len(master_l_date)):
            medianvals_by_date.write(''+str(master_l_date[i][0])+'|'+str(master_l_date[i][1])+'|'
                                     +str(round(statistics.median(d_date[master_l_date[i]])))+'|'
                                     +str(len(d_date[master_l_date[i]]))+'|'
                                     + str(sum(d_date[master_l_date[i]]))
                                     +'\n')
