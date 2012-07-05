from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gstudio.models import *
from objectapp.models import *
import ox
import pandora_client
from gstudio.function import *

def first(request):
	sea=''
	if request.method == "POST":
		#title=request.POST.get('title','')
		#link = request.POST.get('link','')
		#content=request.POST.get('content','')
		#auth = request.POST.get('auth','')
		#sea = request.POST.get('sea','')
		do = request.POST.get('mydropdown','')
		#if sea=='':
		#	m = {'title':title,'slug':'abc','content':content,'status':2,'rurl':link}
		#	q = Gbobject.objects.create(**m)
		#	s = Author.objects.get(username=auth)
		#	q.authors.add(s)
		#	q.save()
		#	a = Objecttype.objects.get(title='VIDEO')		
		#	q.objecttypes.add(Objecttype.objects.get(id=a.id))
		#	q.save()
		#if title=='':
		#	video=Objecttype.objects.get(title="VIDEO")
		#	video = video.get_nbh['contains_members']
		#	video = video.filter(title__contains=sea)	
		#	variables = RequestContext(request,{'video':video})
        	#	template = "gstudio/ChartStudio.html"
        	#	return render_to_response(template, variables)		
		if do!='':
			video = Objecttype.objects.get(title="VIDEO")
			video = video.get_nbh['contains_members']
			if do=='title':
				video = video.order_by(do)
			else:
				video = sort_video(video)				
			variables = RequestContext(request,{'video':video})
        		template = "gstudio/ChartStudio.html"
        		return render_to_response(template, variables)

	video=Objecttype.objects.get(title="VIDEO")
	video = video.get_nbh['contains_members']
	
	api = ox.api.API('http://wetube.gnowledge.org/api')		
	b = api.find({
       'sort': [{
          'key': 'title',
          'operator': '+'
       }],
       'query': {
           'conditions': [
               {
                   'key': 'title',
                   'value': '',
                   'operator': ''
               }
           ],
           'operator': '&'
       },
       'keys': ['id', 'title','user','duration','sourcedescription','created','location'],
       'range': [0,100]
   })
	flag=0
	for each in b['data']['items']:
		a = each['id']
		title = each['title']
		for we in video:
			if we.title==each['title']:
				flag=1
		if flag==0:	
			link = 'http://wetube.gnowledge.org/'+a+'/480p.webm'
			q = Gbobject()
			q.title=each['title']
			q.slug = a
			q.content = ''
			q.status = 2
			q.rurl = link
			q.save()
			a = Objecttype.objects.get(title='VIDEO')		
			q.objecttypes.add(Objecttype.objects.get(id=a.id))
			q.save()
			rel = Attribute()
			rel.attributetype = Attributetype.objects.get(title='time_limit')
			rel.subject = q
			rel.svalue = each['duration']
			rel.save()
			r = Attribute()
			r.attributetype = Attributetype.objects.get(title='source_description')
			r.subject = q
			r.svalue = each['location']
			r.save()
			rel1 = Attribute()
			rel1.attributetype = Attributetype.objects.get(title='posted_by')
			rel1.subject = q
			rel1.svalue = each['user']
			rel1.save()
			rel2 = Attribute()
			rel2.attributetype = Attributetype.objects.get(title='creation_day')
			rel2.subject = q
			rel2.svalue = each['created']
			rel2.save()
			rel3 = Attribute()
			rel3.attributetype = Attributetype.objects.get(title='map_link')
			rel3.subject = q
			m = each['location']
			final = ''
			for each1 in m:
				if each1==" ":
					final=final+'+'
				else:
					final=final+each1
			rel3.svalue = final
			rel3.save()
			q.save()
		flag=0


	video=Objecttype.objects.get(title="VIDEO")
	video = video.get_nbh['contains_members']	
	variables = RequestContext(request,{'video':video})
        template = "gstudio/ChartStudio.html"
        return render_to_response(template, variables)
