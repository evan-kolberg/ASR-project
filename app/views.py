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
def process(request):
    if request.method == 'POST':
        jobid = request.POST.get('jobid')
        userid = request.POST.get('userid')
        cipher_salary = request.POST.get('cipher_salary')
        public_key = request.POST.get('public_key')
        who = request.POST.get('who')

        if who == 'applicant':

            new_applicant = applicant(jobid=jobid, userid=userid,
                                    cipher_salary=cipher_salary,
                                    public_key=public_key)
            new_applicant.save()

            matching_employer = employer.objects.filter(jobid=jobid).first()

            if matching_employer:
                comparison_result = compare_salaries(cipher_salary, matching_employer.cipher_salary, public_key, matching_employer.public_key)

                new_response = responses(jobid=jobid, employerid=matching_employer.userid,
                                        applicantid=userid, boolean=comparison_result, datetime=timezone.now())
                new_response.save()
        
        if who == 'employer':

            new_employer = employer(jobid=jobid, userid=userid,
                                    cipher_salary=cipher_salary,
                                    public_key=public_key)
            new_employer.save()

            matching_applicant = applicant.objects.filter(jobid=jobid).first()

            if matching_applicant:
                comparison_result = compare_salaries(matching_applicant.cipher_salary, cipher_salary, matching_applicant.public_key, public_key)

                new_response = responses(jobid=jobid, employerid=userid,
                                        applicantid=matching_applicant.userid, boolean=comparison_result, datetime=timezone.now())
                new_response.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})




def compare_salaries(applicant_cipher_salary, employer_cipher_salary, applicant_public_key, employer_public_key):
    # Implement Yao's Millionaires' Problem comparison here
    # Compare salary1 and salary2 and return the Boolean result
    return False


