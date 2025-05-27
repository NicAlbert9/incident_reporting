from os import stat
from urllib.request import Request
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import Loginform,incident_reports,ADD_team
from .models import add_team, incident_history,incident_report
from django.db.models import Q
import datetime
from datetime import date
from datetime import datetime
# Create your views here.


#home section
##index_function
def index(request):
    return render(request,"main/index.html")

def admin_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=Loginform(request,request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data["username"]
                upass=fm.cleaned_data["password"]
                user=authenticate(username=uname,password=upass)
                print(user)
                if user is not None:
                    login(request,user)
                    return redirect("/dashboard")

        else:
            fm=Loginform()
        return render(request,"main/a_login.html",{"form":fm})
    else:
        return redirect("/dashboard")

def submit_report(request):
    if request.method=="POST":
        fm=incident_reports(request.POST, request.FILES)
        if fm.is_valid():
            fm.save()
            return redirect("/dashboard")
    else:
        fm=incident_reports()
    return render(request,"main/form_report.html",{"form":fm})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    totalnewequest = incident_report.objects.filter(status__isnull=True).count()
    totalAssign = incident_report.objects.filter(status='Assigned').count()
    totalontheway = incident_report.objects.filter(status='Team On the Way').count()
    totalworkprocess = incident_report.objects.filter(status='Fire Relief Work in Progress').count()
    totalreqcomplete = incident_report.objects.filter(status='Request Completed').count()
    totalfire = incident_report.objects.all().count()
    context={"totalnew":totalnewequest,"assign":totalAssign,"onway":totalontheway,"workprogress":totalworkprocess,"completerequest":totalreqcomplete,"totalfire":totalfire}
    return render(request,"main/dashboard.html",context)

def add_teams(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method=="POST":
        fm=ADD_team(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect("/view_team")
    else:
        fm=ADD_team()
    return render(request,"main/add_team.html",{"form":fm})

def view_team(request):
    if not request.user.is_authenticated:
        return redirect('login')
    fm=add_team.objects.all()
    return render(request,"main/view_team.html",{"form":fm})

def edit_team(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    user=add_team.objects.get(id=id)
    if request.method=="POST":
          fm=ADD_team(request.POST,instance=user)
          if fm.is_valid():
              fm.save()
              return redirect("/view_team")
    else:
        fm=ADD_team(instance=user)
    return render(request,"main/add_team.html",{"form":fm})

def delete_team(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    user=add_team.objects.get(id=id)
    user.delete()
    return redirect("/view_team")

def new_request(request):
    if not request.user.is_authenticated:
        return redirect('login')
    fm=incident_report.objects.filter(status__isnull=True)

    return render(request,"main/new_request.html",{"form":fm})

def view_request(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    team=add_team.objects.all()
    fm=incident_report.objects.get(id=id)
    print(fm)
    reportcount=incident_history.objects.filter(incidentreport=fm).count()
    report1 = incident_history.objects.filter(incidentreport=fm)

    try:
        if request.method=="POST":
            id=request.POST["Assign"]

            status="Assigned"
            team1=add_team.objects.get(id=id)
            now = datetime.now()
            fm.AssignedTime=now.strftime("%m/%d/%y %H:%M:%S")
            fm.AssignTo=team1
            fm.status=status

            fm.save()    
            return redirect("/assign_request1/")      
    except:
        if request.method=="POST":
            status=request.POST["status"]
            remark=request.POST["remark"]
            request_tracking=incident_history.objects.create(incidentreport=fm,status=status,remark=remark)
            fm.status=status
            fm.UpdationDate= date.today()


            fm.save()
            return redirect("/dashboard/")
            #request_tracking.status=status
            #request_tracking.save()
           # report1.status=status
            #report1.save()
           # request_tracking.save()
    return render(request,"main/view_request.html",{"form":fm,"teams":team,"count":reportcount,"report":report1})

def assign_request1(request):
    if not request.user.is_authenticated:
        return redirect('login')
    fm=incident_report.objects.filter(status="Assigned")
    return render(request,"main/assign_request1.html",{"forms":fm})

def team_on_way(request):
    if not request.user.is_authenticated:
        return redirect('login')
    fm=incident_report.objects.filter(status="Team On the Way")
    return render(request,"main/team_way.html",{"form":fm})

def work_in_progress(request):
    if not request.user.is_authenticated:
        return redirect('login')
    fm=incident_report.objects.filter(status="Fire Relief Work in Progress")
    return render(request,"main/work_progress.html",{"form":fm})

def complete_request(request):
    if not request.user.is_authenticated:
        return redirect('login')
    fm=incident_report.objects.filter(status="Request Completed")
    return render(request,"main/complete_request.html",{"form":fm})

def all_request(request):
    if not request.user.is_authenticated:
        return redirect('login')
    fm=incident_report.objects.all()
    return render(request,"main/all_request.html",{"form":fm})


def delete_request(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    user=incident_report.objects.get(id=id)
    user.delete()
    return redirect("/All_Request/")

def Logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    return redirect("/")

def view_status(request):
    info=None
    if request.method=="POST":
        info=request.POST["search"]
    fire=incident_report.objects.filter(Q(mobile=info) | Q(location=info) | Q(name=info))

    return render(request,"main/view_status.html",{"report":fire})


def viw_status_detail(request,pid):
    fm=incident_report.objects.get(id=pid)
    fm2=incident_history.objects.filter(incidentreport=fm)
    count=incident_history.objects.filter(incidentreport=fm).count()
    return render(request,"main/view_status_detail.html",{"form":fm,"form1":fm2,"count":count})


        
