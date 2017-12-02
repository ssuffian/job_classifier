from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import os
import json
import yaml
from bs4 import BeautifulSoup
import requests
from stacklassify.models import Job, JobClassification, Person

# TODO: Add a log-in module so different people can classify the jobs.
# TODO: Add error-handling when it runs out of jobs to classify
# TODO: Add a page that shows three categories: classified-yes jobs, predicted-yes jobs, and all jobs
# TODO: Move scraping scripts out of views.py
# TODO: Push to heroku
# TODO: Add documentation
# TODO: Add unit tests

def scrape_stack():
    url = 'https://stackoverflow.com/jobs/feed'
    job_dir = '../data/jobs/'
    data = requests.get(url)
    soup = BeautifulSoup(data.text,"lxml")
    items = soup.findAll('item')
    num_new_items = 0
    for this_item in items:
        keys = [tag.name for tag in this_item.find_all()]
        output_dict = {}
        for key in keys:
            output_dict[key]=this_item.find(key).text
        output_dict['url']=url
        job_filenames = os.listdir(job_dir)
        if output_dict['guid']+'.json' not in job_filenames:
            with open(job_dir+output_dict['guid']+'.json','w') as f:
                json.dump(output_dict,f,sort_keys = True, indent = 4,
                   ensure_ascii = False)
            Job.objects.create(guid=output_dict['guid'])
            num_new_items +=1
    return len(items),num_new_items

def scrape_remoteio():
    url = 'https://remote.co/remote-jobs/developer/'
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html5lib")
    job_list = soup.findAll(class_='job_listing')
    job_dir = '../data/jobs/'
    num_new_items = 0
    for job in job_list:
        output_dict = {}
        url = job.find('a')['href']
        job_filenames = os.listdir(job_dir)
        if str(hash(url)) + '.json' not in job_filenames:
            data = requests.get(url)
            soup = BeautifulSoup(data.text, "html5lib")
            job_listing = soup.find(class_='job_listing')
            output_dict['title'] = job_listing.find(class_='title_sm').text
            output_dict['category'] = 'remote.io'
            output_dict['description'] = job_listing.find(class_='job_description').text.replace('\n', '<br />')
            output_dict['url'] = url
            output_dict['guid'] = str(hash(url))
            with open(job_dir + output_dict['guid'] + '.json', 'w') as f:
                json.dump(output_dict, f, sort_keys=True, indent=4,
                          ensure_ascii=False)
            Job.objects.create(guid=output_dict['guid'],title=output_dict['title'])
            num_new_items +=1
    return len(job_list),num_new_items

def load_stack(request):
    num_items,num_new_items = scrape_stack()
    return HttpResponse("{} jobs scraped, {} are new.".format(num_items,num_new_items))

def load_remoteio(request):
    num_items,num_new_items = scrape_remoteio()
    return HttpResponse("{} jobs scraped, {} are new.".format(num_items,num_new_items))

def jobs(request):
    #temporary
    this_person = Person.objects.all().get()

    template = loader.get_template('stacklassify/blank.html')
    data_dir = '../data/'
    jobs_dir = data_dir+'jobs/'
    guid = Job.objects.random_new(this_person).guid
    context = {'person_id':this_person.id}
    with open(data_dir+'checkboxes.json','r') as f:
        context.update(json.load(f))
    with open(jobs_dir + guid+'.json', 'r') as f:
        context.update(json.load(f))
    return HttpResponse(template.render(context))

def record(request):
    this_person_id = request.GET['person_id']
    guid = request.GET['guid']
    this_person = Person.objects.get(id=this_person_id)
    this_job = Job.objects.get(guid=guid)
    classification = request.GET.get('classification',False)
    whats_wrong = request.GET.get('whats_wrong',"")
    text_reached = request.GET.get('text_reached',"")
    duration_looked_at = request.GET.get('duration_looked_at')
    JobClassification.objects.create(
        classification="true"==classification,whats_wrong=whats_wrong,
        text_reached=text_reached,duration_looked_at=duration_looked_at,
        job=this_job,
        person=this_person
    )
    Job.objects.get(guid=guid).classified_by.add(this_person)
    return JsonResponse({'status': 'Recorded.'})

def reset(request):
    JobClassification.objects.all().delete()
    [job.classified_by.clear() for job in Job.objects.all()]
    return JsonResponse({'status': 'Updated.'})


def add_person(request):
    Person.objects.create(username="steve",password="test")
    return JsonResponse({'status': 'Updated Person.'})