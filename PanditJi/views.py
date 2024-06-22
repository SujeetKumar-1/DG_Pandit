from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import os
from datetime import date
import random
from django.core.mail import send_mail

from .models import *

# Create your views here.

def home(request):
    crnt_user=request.user
    if crnt_user.is_authenticated:
        if crnt_user.is_people!=True:
            messages.error(request, "You are not a authorised to access this page!")
            return redirect(reverse('userLogin'))
        else:
            return redirect('userdashboard')
        
    allservices=serviceData.objects.all()[:2]
    allservices1=serviceData.objects.all()[2:4]
    panditData=panditProfileData.objects.all()
    return render(request, 'index.html', {'allservices':allservices, 'allservices1':allservices1, 'panditData':panditData})

@login_required(login_url='userLogin')
def userdashboard(request):
    crnt_user=request.user
    if crnt_user.is_people!=True:
        messages.error(request, "You are not a authorised to access this page!")
        return redirect(reverse('userLogin'))

    user_name=crnt_user.name
    context={'user_name':user_name}
    allservices=serviceData.objects.all()[:2]
    allservices1=serviceData.objects.all()[2:4]
    panditData=panditProfileData.objects.all()
    return render(request, 'userDashBoard.html', {'allservices':allservices, 'allservices1':allservices1, 'panditData':panditData, **context})
    
    
def userSignup(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        
        if email is not None:
            if UserAccount.objects.filter(email=email).exists():
                messages.error(request, 'email already exits')
                return redirect('userLogin')
            else:
                user=People.objects.create(email=email)
                user.set_password(pass1)
                user.name=name
                user.user_type="people"
                user.save()
                messages.success(request, "successfully Registered")
                subject='Welcome to Digital Pandit'
                message=f'Hi{user.name}, thank you for registering in DG'
                emailfrom=settings.EMAIL_HOST_USER
                recipient_list=[user.email,]
                send_mail(subject,message, emailfrom, recipient_list)
                return redirect('userLogin')
        
    return render(request, 'signup.html')


def userLogin(request):
    if request.method == 'POST':
        email = request.POST.get('Email')
        pass1 = request.POST.get('pass1')
        
        user = authenticate(request, email=email, password=pass1)
        
        if user is not None:
            login(request, user)
            return redirect('userdashboard')
        else:
            # Handle invalid user
            messages.error(request, 'This email is not registered!')
    
    return render(request, 'signin.html')

def userlogout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='userLogin')
def peopleProfile(request):
    return HttpResponse("Manage your Profile")

@login_required(login_url='userLogin')
def services(request):
    allservice=serviceData.objects.all()
    return render(request, 'services.html', {'allservice':allservice})

@login_required(login_url='userLogin')
def popularPuja(request):
    return render(request, 'popularpuja.html')

@login_required(login_url='userLogin')
def destinationWedding(request):
    return render(request, 'destinationWedding.html')

@login_required(login_url='userLogin')
def contactPage(request):
    return render(request, 'contactpage.html')

@login_required(login_url='userLogin')
def bookPandit(request):
    crnt_user=request.user
    if crnt_user.is_people!=True:
        messages.error(request, "You are not a authorised to access this page!")
        return redirect(reverse('userLogin'))
    context={'user_name':crnt_user.name}
    allservices=serviceData.objects.all()
    panditData=panditProfileData.objects.all()

    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        date=request.POST.get('date')
        time=request.POST.get('time')
        destination=request.POST.get('destination')
        panditName=request.POST.get('pname')
        ritual=request.POST.get('ritual')
        extra=request.POST.get('extra')

        
        sotp=random.randint(1000, 9999)
        subject='confirm booking otp'
        message=f'Hi {name}, confirm your booking of a pandit \n your otp: {sotp}'
        emailfrom=settings.EMAIL_HOST_USER
        recipient_list=[email,]
        sendMail=send_mail(subject,message, emailfrom, recipient_list)

        pooja=serviceData.objects.get(title=ritual)
        if pooja:
            charge=pooja.fee

        bookingDetails={
            'name':name, 'email':email, 
            'phone':phone, 'date':date, 
            'time':time, 'destination':destination, 
            'panditName':panditName, 'ritual':ritual, 
            'extra':extra,
            'sotp':sotp, 'charge':charge
            }

        request.session['booking_details']=bookingDetails
        if sendMail:
            messages.success(request, "otp send your email")
            return redirect('checkoutPage')
        else:
            messages.error(request, "email not found")

    
    return render(request, 'BookingForm.html', {'allservices':allservices, 'panditData':panditData, 'user':crnt_user, **context})


@login_required(login_url='userLogin')
def checkoutPage(request):
    crnt_user=request.user
    if crnt_user.is_people!=True:
        messages.error(request, "You are not a authorised to access this page!")
        return redirect(reverse('userLogin'))
    
    if request.method=='POST':
        otp=request.POST.get('otp')

        booking_details=request.session.get('booking_details')

        if booking_details:
            if booking_details['sotp']==int(otp):
                messages.success(request, "otp verified booking details send your mail")
                subject='Booking Successful!'
                message=f'Dear {booking_details['name']}, Your Booking Request has been send to the Pandit {booking_details['panditName']} \n when pandit accept the bookning request you will get a confirmation mail.'
                emailfrom=settings.EMAIL_HOST_USER
                recipient_list=[booking_details['email'],]
                send_mail(subject,message, emailfrom, recipient_list)
    
                selected_pandit=panditProfileData.objects.get(pname=booking_details['panditName'])
                if selected_pandit:
                    pandit_id=selected_pandit.user
                
                Nuser=People.objects.get(email=crnt_user.email)
                pooja=serviceData.objects.get(title=booking_details['ritual'])

                
                bookingData=Bookings.objects.create(P_user=pandit_id, N_user=Nuser, name=booking_details['name'], ritual_name=booking_details['ritual'], ritual=pooja,
                    phone=booking_details['phone'], ritual_date=booking_details['date'], email=booking_details['email'],
                    ritual_time=booking_details['time'], destination=booking_details['destination'],
                    additional=booking_details['extra'], charge=booking_details['charge'], is_accepted=False
                    )
                bookingData.save()

                
                subject='New Booking Request'
                message=f'Dear {Nuser.name} you have got a new booking request. \n Cleint Name: {booking_details['name']}, Pooja:{booking_details['ritual']} \n Pooja Destination: {booking_details['destination']} \n Date: {booking_details['date']} \n Time: {booking_details['time']} \n login to you dashboard and accept the booking request.'
                emailfrom=settings.EMAIL_HOST_USER
                recipient_list=[Nuser.email,]
                send_mail(subject,message, emailfrom, recipient_list)

                del request.session['booking_details']
                return redirect('historyPage')
            else:
                messages.error(request, "invalid otp")
                return redirect('checkoutPage')
        else:
            return redirect('bookPandit')

    context={'user_name':crnt_user.name}
    bookingDetails = request.session.get('booking_details', {})
    
    return render(request, 'checkout.html', {'user':crnt_user, 'bookings':bookingDetails, **context})


@login_required(login_url='userLogin')
def historyPage(request):
    crnt_user=request.user
    if crnt_user.is_people!=True:
        messages.error(request, "You are not a authorised to access this page!")
        return redirect(reverse('userLogin'))
    

    pendings_bookings=Bookings.objects.filter(N_user=crnt_user.UID, is_accepted=False)
    confirm_bookings=Bookings.objects.filter(N_user=crnt_user.UID, is_accepted=True)
    past_booking=Bookings.objects.filter(N_user=crnt_user.UID, ritual_date__lt=date.today())


    context={'user_name':crnt_user.name}
    return render(request, 'historyPage.html', {'user':crnt_user, 'pendings':pendings_bookings, 'confirm':confirm_bookings, 'past':past_booking, **context})


def searchData(request):
    #if User Search anything on the page
    if request.method=='POST':
        location=request.POST.get('location')
        query=request.POST.get('query')
        result=panditProfileData.objects.filter(skill__contains=query)
        
        return render(request, 'search.html', {'query':query, 'result': result})
    return render(request, 'search.html')







#These views are related to Pandit ji Functionalities
def panditHome(request):
    if request.method=='POST':
        location=request.POST.get('location')
        query=request.POST.get('query')
        result=panditProfileData.objects.filter(skill__contains=query)
    
        return render(request, 'panditHome.html', {'query':query, 'result': result})
    
    return render(request, 'panditHome.html')


def panditSignup(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('pass1')
        if UserAccount.objects.filter(email=email).exists():
            messages.error(request, 'email already exits')
            return redirect('panditLogin')
        else:
            user=Pandit.objects.create(email=email)
            user.user_type="pandit"
            user.name=name
            user.set_password(password)
            user.save()
            messages.success(request, "successfully Registered")
            return redirect('panditLogin')
        
        
    return render(request, 'panditSignup.html')


def panditLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        user = authenticate(request, email=email, password=pass1)
        
        if user is not None:
            login(request, user)
            return redirect('panditdashboard')
        else:
            # Handle invalid user
            messages.error(request, 'Invalid user')

    return render(request, 'panditLogin.html')


def panditlogout(request):
    logout(request)
    return redirect('panditLogin')


@login_required(login_url='panditLogin')
def panditdashboard(request):
    crnt_user=request.user
    if crnt_user.is_authenticated:
        if crnt_user.is_pandit!=True:
            messages.error(request, "You are not a authorised to access this page!")
            return redirect(reverse('panditLogin'))
        
    
    puser=Pandit.objects.get(email=crnt_user.email)
    if panditProfileData.objects.filter(user=puser).exists() is False:
        profile=panditProfileData.objects.create(user=puser)
        profile.save()

    profileimg=panditProfileData.objects.get(user=puser)
    allservice=serviceData.objects.filter(user=puser)[:4]
    user_phone=panditProfileData.objects.get(user=puser)
    context={'user_name':crnt_user.name, 'user_type':crnt_user.user_type, 'gmail':crnt_user.email, 'active':crnt_user.is_active, 'pro_img':profileimg.photo, 'phone':user_phone.phone}
    return render(request, 'Dashboard.html', {'allservice':allservice, **context})


# this function is responsible for update and display profile data to the user end
@login_required(login_url='panditLogin')
def panditProfile(request):
    crnt_user=request.user
    if crnt_user.is_pandit!=True:
        messages.error(request, "You are not a authorised to access this page!")
        return redirect(reverse('panditLogin'))
    
    puser=panditProfileData.objects.get(user=crnt_user.UID)
    if request.method=='POST' and (request.FILES['photo'] and request.FILES['docs']):
        puser.pname=request.POST.get('pname')
        puser.gender=request.POST.get('gender')
        puser.high_edu=request.POST.get('education')
        puser.phone=request.POST.get('phone')
        puser.whatsapp=request.POST.get('wphone')
        puser.country=request.POST.get('country')
        puser.state=request.POST.get('state')
        puser.city=request.POST.get('city')
        puser.pincode=request.POST.get('pincode')
        puser.faddress=request.POST.get('address')
        puser.role=request.POST.get('role')
        puser.experience=request.POST.get('exp')
        puser.lang=request.POST.get('lang')
        puser.skill=request.POST.get('skill')

        supp_docs=request.FILES['docs']
        photo=request.FILES['photo']
        handle_uploaded_file(supp_docs)
        handle_uploaded_file(photo)

        # checking if an image is already uploaded
        if supp_docs and photo:
            if puser.supp_docs:
                existing_img_path=os.path.join(settings.MEDIA_ROOT, str(puser.supp_docs))
                # removing existing image
                if os.path.exists(existing_img_path):
                    os.remove(existing_img_path)
            if puser.photo:
                existing_img_path=os.path.join(settings.MEDIA_ROOT, str(puser.photo))
                # removing existing image
                if os.path.exists(existing_img_path):
                    os.remove(existing_img_path)

        # saving new image file
        puser.supp_docs=supp_docs
        puser.photo=photo

        puser.save()

    userData=panditProfileData.objects.filter(user=crnt_user.UID)
    context={'user_name':crnt_user.name, 'pro_img':puser.photo}
    return render(request, 'profile.html', {'crnt_user':crnt_user, 'userData':userData, **context})


@login_required(login_url='panditLogin')
def servicePage(request):
    crnt_user=request.user
    if crnt_user.is_authenticated:
        if crnt_user.is_pandit!=True:
            messages.error(request, "You are not a authorised to access this page!")
            return redirect(reverse('panditLogin'))
    
    allservices=serviceData.objects.filter(user=crnt_user.UID)
    puser=panditProfileData.objects.get(user=crnt_user.UID)
    context={'user_name':crnt_user.name, 'pro_img':puser.photo}
    return render(request, 'servicesPage.html', {'allservices': allservices, **context})


@login_required(login_url='panditLogin')
def addService(request):
    crnt_user=request.user
    if crnt_user.is_authenticated:
        if crnt_user.is_pandit!=True:
            messages.error(request, "You are not a authorised to access this page!")
            return redirect(reverse('panditLogin'))
    
    user_id=crnt_user.email
    puser=Pandit.objects.get(email=user_id)

    if request.method=='POST' and request.FILES['picture']:
        title=request.POST.get('title')
        desc=request.POST.get('desc')
        fee=request.POST.get('fee')
        service_img=request.FILES['picture']
        handle_uploaded_file(service_img)
        data=serviceData.objects.create(user=puser, title=title, description=desc, fee=fee, service_img=service_img)
        data.save()
    return render(request, 'addService.html')


@login_required
def updateService(request, pk):
    serviceObj=serviceData.objects.get(id=pk)
    if request.method=='POST':
        if request.POST.get('action') == 'delete':
            serviceObj.delete()
            return HttpResponse("Deleted Successfully!")
        else:
            serviceObj.title=request.POST.get('title')
            serviceObj.description=request.POST.get('desc')
            serviceObj.fee=request.POST.get('fee')

            if request.FILES.get('photo'):
                serviceObj.service_img=request.FILES.get('photo')
                serviceObj.save()
                return HttpResponse("Service Updated Successfully!")
            else:
                serviceObj.save()
                return HttpResponse("Service Updated Successfully!")

    return render(request, 'updateService.html', {'service':serviceObj})

def handle_uploaded_file(image):
    with open(os.path.join(settings.MEDIA_ROOT, image.name), 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)
 
@login_required(login_url='panditLogin')
def events(request):
    crnt_user=request.user
    if crnt_user.is_authenticated:
        if crnt_user.is_pandit!=True:
            messages.error(request, "You are not a authorised to access this page!")
            return redirect(reverse('panditLogin'))
        
    pendings_bookings=Bookings.objects.filter(P_user=crnt_user.UID, is_accepted=False)
    confirm_bookings=Bookings.objects.filter(P_user=crnt_user.UID, is_accepted=True)
    past_booking=Bookings.objects.filter(P_user=crnt_user.UID, ritual_date__lt=date.today())
    
    if request.method == 'POST':
        PID = request.POST.get('pid')
        accept = request.POST.get('accept')
        PID=int(PID)
        
        retrive_booking = Bookings.objects.filter(P_user=crnt_user.UID, id=PID).first()

        if retrive_booking:
            if accept == "yes":
                retrive_booking.is_accepted = True
                retrive_booking.save()
                subject = 'New Booking Request'
                message = f'Dear {retrive_booking.name}, your booking request has been confirmed by the pandit.'
                emailfrom = settings.EMAIL_HOST_USER
                recipient_list = [retrive_booking.email]
                send_mail(subject, message, emailfrom, recipient_list)
            elif accept == "no":
                retrive_booking.delete()
                subject = 'Booking Request Rejection'
                message = f'Dear {retrive_booking.name}, your booking request has been rejected by the pandit.'

                # Send email notification
                emailfrom = settings.EMAIL_HOST_USER
                recipient_list = [retrive_booking.email]
                send_mail(subject, message, emailfrom, recipient_list)

    
    user_id=crnt_user.email
    puser=Pandit.objects.get(email=user_id)
    userData=panditProfileData.objects.get(user=crnt_user.UID)
    context={'user_name':puser.name, 'pro_img':userData.photo}
    return render(request, 'event.html', {'user':crnt_user, 'pendings':pendings_bookings, 'confirm':confirm_bookings, 'past':past_booking, **context})

@login_required(login_url='panditLogin')
def notification(request):
    crnt_user=request.user
    if crnt_user.is_authenticated:
        if crnt_user.is_pandit!=True:
            messages.error(request, "You are not a authorised to access this page!")
            return redirect(reverse('panditLogin'))
    
    user_id=crnt_user.email
    puser=Pandit.objects.get(email=user_id)
    userData=panditProfileData.objects.get(user=crnt_user.UID)
    context={'user_name':puser.name, 'pro_img':userData.photo}
    return render(request, 'notification.html', context)

@login_required(login_url='panditLogin')
def resetpassword(request):
    crnt_user=request.user
    if crnt_user.is_authenticated:
        if crnt_user.is_pandit!=True:
            messages.error(request, "You are not a authorised to access this page!")
            return redirect(reverse('panditLogin'))
    
    if request.method =='POST':
        cpass=request.POST.get('cpass')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if check_password(cpass, crnt_user.password):
            if pass1==pass2:
                if cpass==pass1:
                    messages.error(request, "Old Password and new password should not same!")
                crnt_user.set_password(pass1)
                crnt_user.save()
                messages.SUCCESS(request, "Password Reset Successfully!")
                return redirect(reverse('panditLogin'))
            else:
                messages.error(request, "password1 and password2 mismatch!")
        else:
            messages.error(request, "current password is invalid!")

    user_id=crnt_user.email
    puser=Pandit.objects.get(email=user_id)
    userData=panditProfileData.objects.get(user=crnt_user.UID)
    context={'user_name':puser.name, 'pro_img':userData.photo}
    return render(request, 'reset.html', context)

@login_required(login_url='panditLogin')
def help(request):
    crnt_user=request.user
    if crnt_user.is_authenticated:
        if crnt_user.is_pandit!=True:
            messages.error(request, "You are not a authorised to access this page!")
            return redirect(reverse('panditLogin'))
    
    user_id=crnt_user.email
    puser=Pandit.objects.get(email=user_id)
    userData=panditProfileData.objects.get(user=crnt_user.UID)
    context={'user_name':puser.name, 'pro_img':userData.photo}
    return render(request, 'help.html', context)

@login_required(login_url='panditLogin')
def review(request):
    crnt_user=request.user
    if crnt_user.is_authenticated:
        if crnt_user.is_pandit!=True:
            messages.error(request, "You are not a authorised to access this page!")
            return redirect(reverse('panditLogin'))
    
    user_id=crnt_user.email
    puser=Pandit.objects.get(email=user_id)
    userData=panditProfileData.objects.get(user=crnt_user.UID)
    context={'user_name':puser.name, 'pro_img':userData.photo}
    return render(request, 'reviews.html', context)

@login_required(login_url='panditLogin')
def Panditsetting(request):
    crnt_user=request.user
    if crnt_user.is_authenticated:
        if crnt_user.is_pandit!=True:
            messages.error(request, "You are not a authorised to access this page!")
            return redirect(reverse('panditLogin'))
    
    user_id=crnt_user.email
    puser=Pandit.objects.get(email=user_id)
    userData=panditProfileData.objects.get(user=crnt_user.UID)
    context={'user_name':puser.name, 'pro_img':userData.photo}
    return render(request, 'setting.html', context)
