from sklearn.externals import joblib
import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import csv
from csv import writer
from flask import request
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from _datetime import datetime
from django.utils.datastructures import MultiValueDictKeyError
from .models import Document
from .models import Agelife
from .models import Ipdate
from django.shortcuts import render
from django.core import serializers
import json
import test
from django.http import JsonResponse


def index(request):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        print(request.environ['REMOTE_ADDR'])
    else:
        print(request.environ['HTTP_X_FORWARDED_FOR'])
    contextdata={}
    contextdata['resultpath']=''
    contextdata['examplepath'] = '/media/Example_Frailty_Data.csv'
    contextdata['resultdata']=''
    return render(request, 'index.html',contextdata)
def copy_csv(filename):
    df = pd.read_csv(filename)
    # print(df)
    print("df before copy doc///////////////////////////////////////////////////////////////")
    df.to_csv('media/' + 'result.csv', index=False)

def test(request):
    return render(request, 'test.html')

def upload(request):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        print(request.environ['REMOTE_ADDR'])
        ipaddress=request.environ['REMOTE_ADDR']
    else:
        print(request.environ['HTTP_X_FORWARDED_FOR'])
        ipaddress=request.environ['REMOTE_ADDR']
    now=datetime.now()
    print(now)
    current_time=now.strftime("%b %d %Y %H:%M:%S")
    print(current_time)
    contextdata = {}
    if request.method == 'POST':
        try:
            upload_file = request.FILES['document']
            filename = upload_file.name
            fs = FileSystemStorage()
            name = fs.save(upload_file.name, upload_file)
            url = fs.url(name)
            filestyle=url.split(".")
            print(filestyle)
            print(filestyle[-1])
            print("filestyle[-1][0]")
            if filestyle[-1]!='csv':
                contextdata = {
                    'resultdata': '',
                    'examplepath': '/media/Example_Frailty_Data.csv',
                    'resultpath': ''}
                return render(request, 'index.html', contextdata)
            print('filestyle/////////////')
            print(filestyle)
            print("\n\n\n\n\n\n\n\n\n")
            print(url)
            resultdoc = ""
            fileinfo = Document(description=filename, resultdoc=resultdoc, document=url)
            fileinfo.save()
            ipdate=Ipdate(ip=ipaddress, datetime=current_time)
            ipdate.save()
            position = remove_char(url, 0)
            testedgrouplength = getresult(position)
            all_data=Agelife.objects.all()
            totalnumber=len(all_data)
            frighttext=""
            afraidtext=""
            groupnamelist = []
            frightvalue=[]
            afraidvalue=[]
            lastsend=[]
            for i in range(testedgrouplength):
                print("loop parameter values////////////////////")
                print(i)
                eachgroupdata = all_data[totalnumber-testedgrouplength+i]
                frightmean=eachgroupdata.frightmean
                frightmedian=eachgroupdata.frightmedian
                frightstd=eachgroupdata.frightstd
                afraidmean=eachgroupdata.afraidmean
                afraidmedian=eachgroupdata.afraidmedian
                afraidstd=eachgroupdata.afraidstd
                groupname = eachgroupdata.groupname
                frightresult=eachgroupdata.frightresult
                afraidresult=eachgroupdata.afraidresult
                frighteachlist=frightresult.split(",")
                afraideachlist=afraidresult.split(",")
                eachresultdata={
                    'indexvalue':i+1,
                    'frightmean':frightmean,
                    'frightmedian':frightmedian,
                    'frightstd':frightstd,
                    'afraidmean':afraidmean,
                    'afraidmedian':afraidmedian,
                    'afraidstd':afraidstd,
                    'groupname':groupname,
                    'frighteachlist':frighteachlist,
                    'afraideachlist':afraideachlist
                }
                lastsend.append(eachresultdata)
                # print(lastsend)
                for j in range(len(frighteachlist)):
                    groupnamelist.append(groupname)
                # print(groupnamelist)
                frightvalue=frightvalue+frighteachlist
                afraidvalue=afraidvalue+afraideachlist
                # print(frightvalue)
            contextdata={
                'testnumber':testedgrouplength,
                'resultpath': '/media/result.csv',
                'resultdata': lastsend,
                'examplepath': '/media/Example_Frailty_Data.csv'}
            # print(contextdata['resultdata'])
            print(contextdata['resultdata'][0]['frightmean'])
            copy_csv(position)
            csvorigin=pd.read_csv('media/result.csv')
            # print(csvorigin)
            csvorigin.insert(39, 'FRIGHT_age', frightvalue)
            csvorigin.insert(40, 'AFRAID_score', afraidvalue)
            csvorigin.head()
            # print(csvorigin)
            csvorigin.to_csv('media/result.csv', index=False)
            newrows=[ipaddress, current_time]
            append_list_as_row('visitedusers.csv', newrows)
            return render(request, 'index.html', contextdata)
        except MultiValueDictKeyError:
            contextdata={
                'resultdata':'',
                'examplepath':'/media/Example_Frailty_Data.csv',
                'resultpath':''}
            # contextdata['examplepath']='Example_Frailty_Data.csv'
            # print(contextdata)
            return render(request, 'index.html', contextdata)

def remove_char(str, n):
    first_part = str[:n]
    last_part = str[n + 1:]
    return first_part + last_part

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

    # print('///////////////////////////readfile//////////////////////////////')
    # with open('media/ipdate.csv', 'r', newline='') as readFile:
    #     reader = csv.reader(readFile)
    #     lines = list(reader)
    #     numrows=len(lines)
    #     numrowsaa=sum(1 for row in lines)
    #     lines.insert(numrows, row)
    # print(numrows,"numrows")
    # print(numrowsaa,"numrowsaa")
    # print('///////////////////////////writefile//////////////////////////////')
    # with open('visitedusers.csv', 'w') as writeFile:
    #     writer = csv.writer(writeFile)
    #     writer.writerows(lines)
    #
    # readFile.close()
    # writeFile.close()
    # return 0

def getresult(samplefile):
    group=[]
    group.append("group")
    sampleData = pd.read_csv(samplefile)
    # print(sampleData['Group'])
    # print(len(sampleData['Group']))
    for k in sampleData['Group']:
        # print(k)
        # print(str(group[-1:][0]))
        if str(group[-1:][0]) == k:
            print(group)
        else:
            group.append(k)
            # print(group[-1:])
        # print(group)
    group.pop(0)
    # print(group)
    grouplength=len(group)
    frightAge = joblib.load('media/fright_age.sav')
    afraidScore = joblib.load('media/afraid_score.sav')
    frightVariables = ['Tail_stiffening',
                       'Breathing_rate_depth',
                       'Gait_disorders',
                       'Hearing_loss',
                       'Kyphosis',
                       'Tremor',
                       'Body_condition_score',
                       'Forelimb_grip_strength',
                       '%twc',
                       'Menace_reflex',
                       'Alopecia',
                       'Tumours',
                       'Diarrhoea',
                       'Vaginal_uterine_penile_prolapse',
                       'Microphthalmia',
                       'Dermatitis',
                       'Rectal_prolapse',
                       'Distended_abdomen',
                       'Eye_discharge_swelling',
                       'Coat_condition',
                       'Body_Weight_Score']

    afraidVariables = ['Body_Weight_Score',
                       'Alopecia',
                       'Loss_of_fur_colour',
                       'Dermatitis',
                       'Loss_of_whiskers',
                       'Coat_condition',
                       'Tumours',
                       'Distended_abdomen',
                       'Kyphosis',
                       'Tail_stiffening',
                       'Gait_disorders',
                       'Tremor',
                       'Forelimb_grip_strength',
                       'Body_condition_score',
                       'Vestibular_disturbance',
                       'Hearing_loss',
                       'Cataracts',
                       'Corneal_capacity',
                       'Eye_discharge_swelling',
                       'Microphthalmia',
                       'Vision_loss',
                       'Menace_reflex',
                       'Nasal_discharge',
                       'Rectal_prolapse',
                       'Vaginal_uterine_penile_prolapse',
                       'Diarrhoea',
                       'Breathing_rate_depth',
                       'Mouse_grimace_scale',
                       'Piloerection',
                       '%twc',
                       '%rwc',
                       'Thresh_%rwc',
                       'age_days']

    for eachgroup in group:
        testdata = sampleData[(sampleData['Group']==eachgroup)]

        frighteachgroup=frightAge.predict(testdata[frightVariables])
        print('')
        print('FRIGHT age')
        print('')
        print('Median (months)')
        print(eachgroup, round(np.median(frighteachgroup / 30.5), 3))
        frightmedian = round(np.median(frighteachgroup / 30.5), 3)

        print('')
        print('Mean (months)')
        print(eachgroup, round(np.mean(frighteachgroup / 30.5), 3))
        frightmean = round(np.mean(frighteachgroup / 30.5), 3)

        print('Standard deviation (months)')
        print(eachgroup, round(np.std(frighteachgroup / 30.5), 3))
        frightstd = round(np.std(frighteachgroup / 30.5), 3)

        # print('')
        # print('P-value')
        # print(round(stats.ttest_ind(frightControl, frightMr).pvalue, 5))
        # frightp_value = round(stats.ttest_ind(frightControl, frightMr).pvalue, 5)

        afraideachgroup = afraidScore.predict(testdata[afraidVariables])

        print('AFRAID clock')
        print('')
        print('Median (months)')
        print(eachgroup, round(np.median(afraideachgroup / 30.5), 3))
        afraidmedian = round(np.median(afraideachgroup / 30.5), 3)

        print('')
        print('Mean (months)')
        print(eachgroup, round(np.mean(afraideachgroup / 30.5), 3))
        afraidmean = round(np.mean(afraideachgroup / 30.5), 3)

        print('')
        print('Standard deviation (months)')
        print(eachgroup, round(np.std(afraideachgroup / 30.5), 3))
        afraidstd = round(np.std(afraideachgroup / 30.5), 3)
        print('')

        list(frighteachgroup)
        list(afraideachgroup)
        frightresult=','.join(map(str, frighteachgroup))
        afraidresult=','.join(map(str, afraideachgroup))
        eachresult=Agelife(groupname=eachgroup, frightmedian=frightmedian, frightmean=frightmean, frightstd=frightstd, afraidmedian=afraidmedian, afraidmean=afraidmean, afraidstd=afraidstd, frightresult=frightresult, afraidresult=afraidresult)
        eachresult.save()
    return grouplength

def getavg(listvalue):
    total=0
    listvalueavg=0
    for ele in range(0, len(listvalue)):
        total = total + listvalue[ele]
    print(total)
    listvalueavg = total / len(listvalue)
    maxvalue=0
    minvalue=0
    maxvalue=max(listvalue)
    minvalue=min(listvalue)
    listvalue_result=[]
    listvalue_result = [minvalue, listvalueavg, maxvalue]
    return listvalue_result

def graphdata(request):
    alldata = Agelife.objects.all()
    # print(alldata)
    alldatacount=len(alldata)
    # print(alldatacount)
    groupcount=int(request.GET['testnumber'])
    # print(groupcount)
    frightlist=[]
    afraidlist=[]
    namelist=[]
    for i in range(groupcount):
        frightresult=alldata[alldatacount-groupcount+i].frightresult
        afraidresult=alldata[alldatacount-groupcount+i].afraidresult
        groupname=alldata[alldatacount-groupcount+i].groupname
        frightlist.append(frightresult)
        afraidlist.append(afraidresult)
        namelist.append(groupname)
        # print(frightresult)
        # print(afraidlist)
    contextdata={
        'namelist': namelist,
        'frightlist': frightlist,
        'afraidlist': afraidlist
    }
    contextdata = json.dumps(contextdata)
    # print(contextdata)
    return HttpResponse(contextdata, content_type='application/json')
