from email import message
from lib2to3.pgen2 import token
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from owner.models import Applicants, Candidates, Marks, Subjects
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from django.contrib.auth import views as auth_views


# Create your views here.

#Coded by Hana
def register(request):
    if request.method == 'POST':


        Name = request.POST['Name']
        Age = request.POST['Age']
        Gender = request.POST['Gender']
        Address = request.POST['Address']
        Mob = request.POST['Mob']
        Email = request.POST['Email']
        Department = request.POST['Department']
        University = request.POST['University']
        SubjectName = request.POST['subject']
        Dob = request.POST['Dob']
        Phd_Reg = request.POST['Phd_Reg']
        Phd_Joining_Date = request.POST['Phd_Joining_Date']
        Research_Topic = request.POST['Research_Topic']
        Research_Guide = request.POST['Research_Guide']
        Guide_Mail = request.POST['Guide_Mail']
        Guide_Phone = request.POST['Guide_Phone']

        # if Applicants.objects.filter(Email=Email).exists():
        #     return JsonResponse(
        #         {'success': 'error'},
        #         safe=False
        #     )
        # else:

        user_obj = Applicants()
        user_obj.Name = Name
        user_obj.Age = Age
        user_obj.Gender = Gender
        user_obj.Address = Address
        user_obj.Mob = Mob
        user_obj.Email = Email
        user_obj.Subject = SubjectName
        user_obj.Department = Department
        user_obj.University = University
        user_obj.Dob = Dob
        user_obj.Phd_Reg = Phd_Reg
        user_obj.Phd_Joining_Date = Phd_Joining_Date
        user_obj.Research_Topic = Research_Topic
        user_obj.Research_Guide = Research_Guide
        user_obj.Guide_Mail = Guide_Mail
        user_obj.Guide_Phone = Guide_Phone


        user_obj.save()

        return redirect('/user/regSuccess')

            # return JsonResponse(
            #
            #     {'success': 'pass'},
            #     safe=False
            # )

    else:

        subjects=Subjects.objects.all()
        return render(request, 'user/register_section/register_form.html',{'subjects':subjects})


def reg_success(request):
    return render(request, 'user/register_section/reg_complete.html')


# Sharun
def login(request):
    # if request.method == 'POST':
    #     username = request.POST['Username']
    #     password = request.POST['Password']
    #     print(username, password)
    #
    #     user = auth.authenticate(username=username, password=password)
    #
    #     if user is not None:
    #         auth.login(request, user)
    #         request.session['username'] = username
    #         return redirect('/user/dashboard')
    #     else:
    #         messages.info(request, 'Invalid credentials')
    #         return redirect('/user/login')
    #
    # else:
    #     return render(request, 'user/auth/login.html')


    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            return JsonResponse(
                {'success': True},
                safe=False
            )

        else:

            print("Invalid Credentials")
            return JsonResponse(
                {'success': False},
                safe=False
            )

    else:
        return render(request, 'user/auth/login.html')



def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('/user/login')


def dashboard(request):
    if 'username' in request.session:
        User = Candidates.objects.get(RegNumber=request.session['username'])
        # Username = User.ApplicationId.Name
        return render(request, 'user/dashboard.html', {'User': User})
    else:
        return redirect('/user/login')


def payment_form(request):
    if 'username' in request.session:
        user = Candidates.objects.get(RegNumber=request.session['username'])

        if request.method == 'POST':
            if len(request.FILES['File']) != 0:
                PaymentDetails = request.FILES['File']
                user.PaymentDetails = PaymentDetails
                user.save()
                Uploaded_file = user.PaymentDetails
            # return redirect('/user/payment_form')
            return render(request, 'user/payment_form.html', {'Uploaded_file': Uploaded_file,'message': "Successfully uploaded Payment Details"} )
        else:
            Uploaded_file = user.PaymentDetails
            return render(request, 'user/payment_form.html', {'Uploaded_file': Uploaded_file})
    else:
        return redirect('/user/login')

    return render(request, 'user/dashboard.html')


# coded By Rohith (For validating email within the browser itself)
def validate_email(request):
    email_received = request.GET.get('email', None)
    data = {
        'is_taken': Applicants.objects.filter(Email=email_received).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this email already exists.'
    return JsonResponse(data)

    return render(request, 'user/dashboard.html')



#coded by Hana
def marks(request):
    if 'username' in request.session:
        User = Candidates.objects.get(RegNumber=request.session['username'])
        marks = Marks.objects.all()
        return render(request, 'user/marks.html',{ 'User':User,'marks':marks})
    else:
        return redirect('/user/login')


#coded by Akhila
def attendance(request):
    if 'username' in request.session:
        User = Candidates.objects.get(RegNumber=request.session['username'])
        attendance= Marks.objects.all()

    return render(request, 'user/attendance.html',{ 'User':User,'attendance':attendance})

#Coded by Hana

def settings(request):
    if 'username' in request.session:
        User = Candidates.objects.get(RegNumber=request.session['username'])

        return render(request, 'user/settings.html',{'User':User})

def password_change_alert(request):
    if request.session.has_key('username'):
        user = Candidates.objects.get(RegNumber=request.session['username'])
        return render(request,'user/dashboard.html', {'User': user, 'message': "Password changed successfully"})

def change_password(request):

    if request.session.has_key('username'):

        if request.method == 'POST':

            Password = request.POST['password']

            user = Candidates.objects.get(RegNumber=request.session['username'])
            u = User.objects.get(username=user.RegNumber)
            u.set_password(Password)
            u.save()
            return JsonResponse(
                    {'success': True},
                    safe=False
                )
    else:
        return render(request, 'settings.html')

def photo_upload(request):
    if 'username' in request.session:
        user = Candidates.objects.get(RegNumber=request.session['username'])
        if request.method == 'POST':
            if len(request.FILES['File']) != 0:
                Photo = request.FILES['File']
                user.Photo = Photo
                user.save()
               # return redirect('/user/dashboard')
                return render(request, 'user/dashboard.html', {'User': user, 'message': "Successfully uploaded your photo"})
            else:
                return render(request, 'user/dashboard.html', {'User': user,'message':"Please upload your Photo"})
        else:

            return render(request, 'user/dashboard.html', {'User': user,'message':"uploaded"})
    else:
        return redirect('/user/login')

    return render(request, 'user/dashboard.html')



# Coded By Rohith
# For custom 404 and 500 error page
def handler404(request, exception):
    return render(request, 'reusable/page_404.html', status=404)


def handler500(request, exception):
    return render(request, 'reusable/page_404.html', status=500)


