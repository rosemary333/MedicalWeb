# -*- coding:UTF-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import demjson
from db_method import insert,select,update,delete
from control_method import tools
from django.shortcuts import render
from django.contrib import auth
from Website.models import AttachInfo
from django.conf import settings
import datetime, random



def PermissionCheck(function_type = 1):
    def deco(func):
        def wrapper(request):
            if request.method == 'POST':
                data = request.POST
            else:
                data = request.GET
            D_id = request.session['_auth_user_id']
            user_type = select.getUserGroup(D_id)
            print user_type,function_type
            if user_type > function_type:
                return HttpResponse(status=403)

            print "success"
            return func(request,data,D_id)
        return wrapper
    return deco

@login_required
@csrf_exempt
def getUserGroup(request):
    message = {'result': -1}
    if request.method == 'GET':
        data = request.GET
    D_id = request.session['_auth_user_id']
    user_type = select.getUserGroup(D_id)
    message['result'] = str(user_type)
    js = json.dumps(message)
    return HttpResponse(js)

#接口1
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = request.POST
        print data['code']
        if select.checkCode(data['code']):
            print "inside"
            message = {'result': -1}
            if insert.addUserInfo(data) == True:
                message['result'] = 0
            else:
                message['result'] = -1
        else:
            message = {'result': -1}
        message = tools.toString(message)
        js = json.dumps(message)
        return HttpResponse(js)

#接口2
@csrf_exempt
def repeatCheck(request):
    if request.method == 'POST':
        message = {'result': -1}
        data = request.POST
        if select.checkExist(data['key'],data['value']):
            result = -1
        else:
            result = 0

        # message = tools.toString(message)
        js = json.dumps(message)

        return HttpResponse(js)
#接口3
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = request.POST
        message = {"result":"-1"}
        username = request.POST.get('userName','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)

        #判断用户名是否存在
        if user is not None and user.is_active:
            print user
            auth.login(request,user)
            message['result'] = 0

        # message={'result':-1}
        # if select.checkExist('userName',data['userName']):
        #     message['result'] = 0
        #     request.session['_auth_user_id'] = select.getUserInfo(data['userName'], 'D_id')
        #     print request.session['_auth_user_id']
        # else:
        #     message['result'] = -1
        message = tools.toString(message)
        js =  json.dumps(message)

        return HttpResponse(js)

# 接口4
@login_required
@csrf_exempt
def retrievePassword(request):
    if request.method == 'POST':
        message = {'result': -1}
        data = request.POST
        # mail
        if int(data['type']) == 1:
            if data['mail_cellphone'] == select.getUserInfo(data['userName'], 'mail'):
                if tools.sendEmail(data['mail_cellphone'],
                                    select.getUserInfo(data['userName'], 'password')) == True:
                    result = 0
                else:
                    result = -1
            else:
                result = -1
        # cellphone
        else:
            if data['mail_cellphone'] == select.getUserInfo(data['userName'], 'cellphone'):
                result = 0
                # TODO
            else:
                result = -1
        # message = tools.toString(message)
        js = json.dumps(message)
        return HttpResponse(js)

#接口5
@login_required
@PermissionCheck(3)
@csrf_exempt
def getDoctorBasicInfo(request,data,D_id):
    print "aaa"
    message = select.getDoctorBasicInfo(D_id)
    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)

#接口6
@login_required
@PermissionCheck(3)
@csrf_exempt
def getDoctorDetailedInfo(request,data,D_id):
    message = select.getDoctorDetailedInfo(D_id)
    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


#接口7
@login_required
@PermissionCheck(2)
@csrf_exempt
def updateDoctorInfo(request,data,D_id):
    message = {}
    if update.updateUserInfo(D_id,data) == True:
        message['result'] = 0
    else:
        message['result'] = -1

    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


#接口8
@login_required
@PermissionCheck(3)
@csrf_exempt
def getExpGroups(request,data,D_id):
    message = []
    print D_id
    message = select.getExpGroups(D_id)
    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)

#接口9
@login_required
@PermissionCheck(3)
@csrf_exempt
def getExpGroupPatientsInfo(request,data,D_id):
    message = []
    message = select.getExpGroupPatientsInfo(int(data['G_id']))
    # message = tools.toString(message)
    js = json.dumps(message)
    print js
    return HttpResponse(js)

@login_required
@PermissionCheck(3)
@csrf_exempt
def getOneExpGroupInfo(request,data,D_id):
    message = []
    message = select.getOneExpGroupInfo(int(data['G_id']))
    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)



#接口10
@login_required
@PermissionCheck(2)
@csrf_exempt
def addOrUpdateExpGroup(request,data,D_id):
    message = {}

    if data['G_id'] == '':
        if insert.addExpGroup(D_id,data['name'],data['description'], data['date']) == True:
            message['result'] = 0
        else:
            message['result'] = -1
    else:
        if update.updateExpGroup(int(data['G_id']), data['name'], data['description'], data['date']) == True:
            message['result'] = 0
        else:
            message['result'] = -1
    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)

#接口11
@login_required
@PermissionCheck(1)
@csrf_exempt
def deleteExpGroup(request,data,D_id):
    message = {}
    if delete.deleteExpGroup(D_id,int(data['G_id'])) == True:
        message['result'] = 0
    else:
        message['result'] = -1
    message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


# for add
@login_required
@PermissionCheck(3)
@csrf_exempt
def getPatientGroupInfo(request,data,D_id):
    message = {}
    list =[]
    pglist =[]
    G_id = data['G_id']
    temp = select.getExpGroupPatientsID(G_id)
    for item in temp:
        pglist.append(item[0])
    patientlist = select.getPatientsBasicInfo()
    print patientlist
    for patient in patientlist:
        print patient['P_id'],"patient"
        if patient['P_id'] not in pglist:
            list.append(patient)

    js = json.dumps(list)
    return HttpResponse(js)


#接口13
@login_required
@PermissionCheck(2)
@csrf_exempt
def addPatientToExpGroup(request,data,D_id):
    message = {}
    data1 = tools.forCheckbox2(data, 'add')
    if insert.addPatientToExpGroup(int(data['G_id']),data1):
        message['result'] = 0
    else:
        message['result'] = -1
    message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)

#接口14
@login_required
@PermissionCheck(1)
@csrf_exempt
def removePatientfromExpGroup(request,data,D_id):
    message = {}
    if delete.removePatientfromExpGroup(int(data['G_id']),data['P_id']):
        message['result'] = 0
    else:
        message['result'] = -1
    message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)

#接口15
@login_required
@PermissionCheck(3)
@csrf_exempt
def getPatientsBasicInfo(request,data,D_id):
    message = []
    message = select.getPatientsBasicInfo()
    js = json.dumps(message)
    return HttpResponse(js)

#接口16
@login_required
@PermissionCheck(3)
@csrf_exempt
def getPatientDetailedInfo(request,data,D_id):
    message = []
    message = select.getPatientDetailedInfo(data['P_id'])
    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)

            


#接口17
@login_required
@PermissionCheck(2)
@csrf_exempt
def addOrUpdatePatientInfo(request,data,D_id):
    message = {}

    if data['id'] == '':
        if insert.addPatientInfo(data) == True:
            message['result'] = 0
        else:
            message['result'] = -1
    else:
        if update.updatePatientInfo(data) == True:
            message['result'] = 0
        else:
            message['result'] = -1
    message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


# #接口18
# @login_required
#@csrf_exempt
# def updatePatientInfo(request):
#     if request.method == 'POST':
#         message = {}
#         data = request.POST
#         
#             D_id = request.session['_auth_user_id']
#             if update.updatePatientInfo(data) == True:
#                 message['result'] = 0
#             else:
#                 message['result'] = -1
#             # message = tools.toString(message)
#             js = json.dumps(message)
#             return HttpResponse(js)
#         else:
#             

#接口19
@login_required
@PermissionCheck(3)
@csrf_exempt
def getRelationsInfo(request,data,D_id):
    message = []
    message = select.getRelationInfos(data['P_id'])
    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


# #接口20
# @login_required
#@csrf_exempt
# def updateRelationInfo(request):
#     if request.method == 'POST':
#         message = {}
#         data = request.POST
#         
#             D_id = request.session['_auth_user_id']
#             R_id = int(data['R_id'])
#             if update.updateRelationInfo(R_id,data) == True:
#                 message['result'] = 0
#             else:
#                 message['result'] = -1
#             # message = tools.toString(message)
#             js = json.dumps(message)
#             return HttpResponse(js)
#         else:
#             

#接口21
@login_required
@PermissionCheck(2)
@csrf_exempt
def addOrUpdateRelationInfo(request,data,D_id):
    message = {}

    if data['R_id'] == '':
        if insert.addRelationInfo(data) == True:
            message['result'] = 0
        else:
            message['result'] = -1
    else:
        R_id = int(data['R_id'])
        if update.updateRelationInfo(R_id, data) == True:
            message['result'] = 0
        else:
            message['result'] = -1

    message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


#接口22
@login_required
@PermissionCheck(1)
@csrf_exempt
def deleteRelation(request,data,D_id):
    message = {}
    if delete.deleteRelation(int(data['R_id'])) == True:
        message['result'] = 0
    else:
        message['result'] = -1
    message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)



@login_required
@PermissionCheck(3)
@csrf_exempt
def getCEHAllInfo(request,data,D_id):
    message = []
    if int(data['type']) == 0:
        message = select.getPatientAllOutPatientServiceInfos(data['P_id'])
    elif int(data['type']) == 1:
        message = select.getPatientAllEmergCallInfos(data['P_id'])
    elif int(data['type']) == 2:
        message = select.getPatientAllInHospitalInfos( data['P_id'])

    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


#接口23
@login_required
@PermissionCheck(3)
@csrf_exempt
def getCEHDetailedInfo(request,data,D_id):
    message = []
    if int(data['type']) == 0:
        message = select.getPatientDetailedOutPatientServiceInfos(data['S_id'])
    elif int(data['type']) == 1:
        message = select.getPatientDetailedEmergCallInfos(data['S_id'])
    elif int(data['type']) == 2:
        message = select.getPatientDetailedInHospitalInfos( data['S_id'])

    #message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


#接口24
@login_required
@PermissionCheck(2)
@csrf_exempt
def addOrUpdateCEHInfo(request,data,D_id):
    message = {'result':-1}

    if data['id'] == '':
        if int(data['type']) == 0:
            result = insert.addOutPatientServiceInfo(data)
        elif int(data['type']) == 1:
            result = insert.addEmergCallInfo(data)
        elif int(data['type']) == 2:
            result = insert.addInHospitalInfo(data)
        else:
            result = False
    else:
        id = int(data['id'])
        if int(data['type']) == 0:
            result = update.updateOutPatientServiceInfo(id, data)
        elif int(data['type']) == 1:
            result = update.updateEmergCallInfo(id, data)
        elif int(data['type']) == 2:
            result = update.updateInHospitalInfo(id, data)
        else:
            result = False

    if result == True:
        message['result'] = 0

    message = tools.toString(message)
    js = json.dumps(message)
    print js,"########"
    return HttpResponse(js)


#接口25
@login_required
@PermissionCheck(1)
@csrf_exempt
def deleteCEHInfo(request,data,D_id):
    message = {'result':-1}
    if int(data['type']) == 0:
        result = delete.deleteOutPatientServiceInfo(int(data['S_id']))
    elif int(data['type']) == 1:
        result = delete.deleteEmergCallInfo(int(data['S_id']))
    elif int(data['type']) == 2:
        result = delete.deleteInHospitalInfo(int(data['S_id']))
    else:
        result = False

    if result == True:
        message['result'] = 0

    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)

# #接口26
# @login_required
@csrf_exempt
# def updateCEHInfo(request):
#     if request.method == 'POST':
#         data = request.POST
#         message = {'result':-1}
#         
#             D_id = request.session['_auth_user_id']
#             id = int(data['id'])
#             if int(data['type']) == 0:
#                 result = update.updateOutPatientServiceInfo(id,data)
#             elif int(data['type']) == 1:
#                 result = update.updateEmergCallInfo(id,data)
#             elif int(data['type']) == 2:
#                 result = update.updateInHospitalInfo(id,data)
#             else:
#                 result = False
#
#             if result == True:
#                 message['result'] = 0
#
#             # message = tools.toString(message)
#             js = json.dumps(message)
#             return HttpResponse(js)
#         


# 接口27
@login_required
@PermissionCheck(3)
@csrf_exempt
def getCorQBasicInfo(request,data,D_id):
    message = []
    if int(data['kind']) == 0:
        message = select.getBasicClinicInfos(data['type'],int(data['S_id']))
    else:
        message = select.getBasicQuestionnaireInfos(data['type'],int(data['S_id']))

    # message = tools.toString(message)
    js = json.dumps(message)
    print js
    return HttpResponse(js)


# 接口28
@login_required
@PermissionCheck(3)
@csrf_exempt
def getClinicDetailedInfo(request,data,D_id):
    message = select.getDetailedClinicInfo(int(data['Cli_id']))

    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)

# 接口29
@login_required
@PermissionCheck(3)
@csrf_exempt
def getQuestionnaireDetailedInfo(request,data,D_id):
    message = select.getDetailedQuestionnaireInfo(int(data['type']),int(data['id']))
    # message = tools.toString(message)
    js = json.dumps(message)
    print js
    return HttpResponse(js)



# 接口30
@login_required
@PermissionCheck(2)
@csrf_exempt
def addOrUpdateClinicInfo(request,data,D_id):
    message = {'result': -1}
    S_id = int(data['S_id'])
    if data['Cli_id'] == '':
        if insert.addClinicInfo(S_id,data):
            message['result'] = 0
    else:
        if update.updateClinicInfo(data):
            message['result'] = 0
    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


# 接口31
@login_required
@PermissionCheck(2)
@csrf_exempt
def addOrUpdateQuestionnaireInfo(request,data,D_id):
    message = {'result': -1}
    S_id = int(data['S_id'])
    kind = int(data['kind'])

    if ('ESS_id' in data and data['ESS_id']=='') or \
        ('MBQ_id' in data and data['MBQ_id']=='') or \
        ('SGRQ_id' in data and data['SGRQ_id']==''):

        if insert.addQuestionnaireInfo(kind,S_id,data):
            message['result'] = 0

    else:
        if update.updateQuestionnaireInfo(kind, S_id, data):
            message['result'] = 0

    message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)

# 接口34
@login_required
@PermissionCheck(1)
@csrf_exempt
def deleteClinicInfo(request,data,D_id):
    message = {'result': -1}
    if delete.deleteClinicInfo(int(data['Cli_id'])):
        message['result'] = 0
    message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


# 接口35
@login_required
@PermissionCheck(1)
@csrf_exempt
def deleteQuestionnaireInfo(request,data,D_id):
    message = {'result': -1}
    if delete.deleteQuestionnaireInfo(int(data['kind']),int(data['id'])):
        message['result'] = 0
    # message = tools.toString(message)
    js = json.dumps(message)
    print js
    return HttpResponse(js)



# 接口36
@login_required
@PermissionCheck(3)
@csrf_exempt
def getAorAEDetailedInfo(request,data,D_id):
    message = []
    if int(data['kind']) == 0:
        message = select.getDetailedAccessoryExamination(data['type'],int(data['S_id']))
    else:
        message = select.getDetailedAttachInfos(data['type'],int(data['S_id']))
    js = json.dumps(message)
    return HttpResponse(js)



@login_required
@PermissionCheck(3)
@csrf_exempt
def getOneAorAEDetailedInfo(request,data,D_id):
    message = []
    if int(data['kind']) == 0:
        message = select.getOneDetailedAccessoryExamination(int(data['AE_id']))
    else:
        message = select.getOneDetailedAttachInfos(int(data['A_id']))

    # message = tools.toString(message)
    js = json.dumps(message)
    print js
    return HttpResponse(js)


# 接口37
@login_required
@PermissionCheck(2)
@csrf_exempt
def addOrUpdateAorAEDetailedInfo(request,data,D_id):
    myFile = request.FILES.get("myimage",None)
    print myFile
    message = {'result': -1}
    S_id = int(data['S_id'])
    if ('A_id' in data and data['A_id']=='') or \
        ('AE_id' in data and data['AE_id']=='') :
        if not myFile:
            return HttpResponse("no files for upload!")
        if int(data['kind']) == 0:
            if insert.addAccessoryExamination(D_id, S_id, data, myFile):
                message['result'] = 0
        else:
            if insert.addAttachInfo(D_id, S_id, data, myFile):
                message['result'] = 0
    else:
        if int(data['kind']) == 0:
            if update.updateAccessoryExamination(int(data['AE_id']), D_id, S_id, data, myFile):
                message['result'] = 0
        else:
            if update.updateAttachInfo(int(data['A_id']), D_id, S_id, data, myFile):
                message['result'] = 0

    js = json.dumps(message)
    return HttpResponse(js)

# 接口39
@login_required
@PermissionCheck(1)
@csrf_exempt
def deleteAorAEDetailedInfo(request,data,D_id):
    message = {'result': -1}
    if int(data['kind']) == 0:
        if delete.deleteAccessoryExamination(int(data['id'])):
            message['result'] = 0
    else:
        if delete.deleteAttachInfo(int(data['id'])):
            message['result'] = 0

    message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


# 接口40
@login_required
@PermissionCheck(2)
@csrf_exempt
def updateDocPassword(request,data,D_id):
    message = {}
    if update.updatePassword(D_id, data['oldPassword'],data['newPassword']):
        message['result'] = 0
    else:
        message['result'] = -1
    message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


# 接口41
# Cat &&MRC 返回近两周的sum
@login_required
@PermissionCheck(3)
@csrf_exempt
def getCat_MRCSum2Weeks(request,data,D_id):
    message = []
    message = select.getMsg2Weeks(data['P_id'], 1)

    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)

# 接口42
# 近两周暴露水平
@login_required
@PermissionCheck(3)
@csrf_exempt
def getExploure2Weeks(request,data,D_id):
    message = []
    message = select.getMsg2Weeks(data['P_id'], 2)
    # message = tools.toString(message)
    js = json.dumps(message)
    return HttpResponse(js)


# 接口43
@login_required
@PermissionCheck(3)
@csrf_exempt
def getPatientName(request,data,D_id):
    message = {}
    message = select.getPatientName(data['P_id'])
    js = json.dumps(message)
    return HttpResponse(js)



#APP interface 1
@csrf_exempt
def app_login(request):
    if request.method == 'POST':
        data = request.POST
        print data,"loginnnnnnnnn"
        message = {}
        message['result'] = select.patientLogin(data['P_id'],data['password'])
        return HttpResponse(json.dumps(message))


#APP interface 2
@csrf_exempt
def app_addOrUpdateCATTable(request):
    if request.method == 'POST':
        data = request.POST
        print data,"CATTTTTTTTTTTTTTTT"
        message = {'result':'-1','id':'-1'}
        if data['id'] == '':
            message['id'] = insert.addCATandMRC(data)
        else:
            message['id'] = update.updateCATandMRC(data)
        if message['id'] != -1:
            message['result'] = '0'

        return HttpResponse(json.dumps(message))

#APP interface 3
@csrf_exempt
def app_addOrUpdatePmExposureTable(request):
    if request.method == 'POST':
        data = request.POST
        print data, "PMEEEEEEEEEEEEEE"
        message = {'result': '-1', 'id': '-1'}
        if data['id'] == '':
            message['id'] = insert.addPmExposure(data)
        else:
            message['id'] = update.updatePmExposure(data)
        if message['id'] != -1:
            message['result'] = '0'
        return HttpResponse(json.dumps(message))

#APP interface 4
@csrf_exempt
def app_addOrUpdateTrackInfoTable(request):
    if request.method == 'POST':
        data = request.POST
        print data, "Trackkkkkkkkkkkk"
        message = {'result': '-1', 'id': '-1'}
        if data['id'] == '':
            message['id'] = insert.addTrackInfo(data)
        else:
            message['id'] = update.updateTrackInfo(data)
        if message['id'] != -1:
            message['result'] = '0'
        return HttpResponse(json.dumps(message))


#APP interface 5
@csrf_exempt
def app_addOrUpdateMedicineRegularTable(request):
    if request.method == 'POST':
        data = request.POST
        print data,"Medicineeeeee"
        message = {'result': '-1', 'id': '-1'}
        if data['id'] == '':
            message['id'] = insert.addMedicineRegular(data)
        else:
            message['id'] = update.updateMedicineRegular(data)
        if message['id'] != -1:
            message['result'] = '0'


#APP interface 6
@csrf_exempt
def app_addOrUpdateMedicineChangeTable(request):
    if request.method == 'POST':
        data = request.POST
        message = {'result': '-1', 'id': '-1'}
        if data['id'] == '':
            message['id'] = insert.addMedicineChange(data)
        else:
            message['id'] = update.updateMedicineChange(data)
        if message['id'] != -1:
            message['result'] = '0'
        return HttpResponse(json.dumps(message))

#APP interface 7
@csrf_exempt
def app_addOrUpdateMedicineRecordTable(request):
    if request.method == 'POST':
        data = request.POST
        message = {'result': '-1', 'id': '-1'}
        if data['id'] == '':
            message['id'] = insert.addMedicineRecord(data)
        else:
            message['id'] = update.updateMedicineRecord(data)
        if message['id'] != -1:
            message['result'] = '0'
        return HttpResponse(json.dumps(message))

# 接口43
@login_required
@PermissionCheck(3)
@csrf_exempt
def test(request):
    print "test-inside"

    if request.method == 'POST':
        data = request.POST
        print data['P_id']
        print data['a']
        message = {'result':'1',"a":"sa"}
        print data
        return HttpResponse(json.dumps(message))
        #return HttpResponse(message)

    else:
        data = request.GET
        message = {'result':'-1'}
        print data
        return HttpResponse(json.dumps(message))

def test2(request):

    return render(request,"form-dropzone.html")

@csrf_exempt
def upload2(request):
    if request.method == 'POST':
        data = request.POST
        print data
        myFile = request.FILES['upload_file']
        D_id = int("4")
        message = {'result': -1}
        obj = AttachInfo(type ="0", name = tools.md5(str(random.randint(0,9))+str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))),doc = myFile,date = datetime.datetime.strptime("2016-04-08", "%Y-%m-%d").date(), D_id = D_id, S_id = int("1"), P_id = "0000000001")
        obj.save()
        print request.FILES,"FILES"
        js = json.dumps(message)
        return HttpResponse(js)


@login_required
@PermissionCheck(1)
@csrf_exempt
def addInvitation(request,data,D_id):
    print "wew"
    if insert.addInvitation(D_id,data):
        js = json.dumps({"result":"0"})
    else:
        js = json.dumps({"result":"-1"})
    return HttpResponse(js)

@login_required
@PermissionCheck(1)
@csrf_exempt
def getInvitation(request,data,D_id):
    message = select.getInvitation()
    print message
    js = json.dumps(message)
    return HttpResponse(js)

@login_required
@PermissionCheck(1)
@csrf_exempt
def deleteInvitation(request,data,D_id):
    result = -1
    if delete.deleteInvitation(data):
        result = 0
    js = json.dumps({"result":result})
    return HttpResponse(js)
