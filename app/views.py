from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import employer, applicant, responses
from django.utils import timezone


def handle(request):
    return render(request, 'index.html')

def handle_applicant(request):
    return render(request, 'applicant.html')

def handle_employer(request):
    return render(request, 'employer.html')



@csrf_exempt
def applicant_submit(request):
    if request.method == 'POST':
        jobid = request.POST.get('jobid')
        applicantid = request.POST.get('applicantid')
        salary = request.POST.get('salary')

        new_applicant = applicant(jobid=jobid, applicantid=applicantid, salary=salary)
        new_applicant.save()  
        
            
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})




@csrf_exempt
def employer_submit(request):
    if request.method == 'POST':
        

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

