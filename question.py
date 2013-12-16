#!/usr/bin/python

import cgitb, cgi, MySQLdb, ast
#import cgitb, cgi, ast
import cPickle as p
from random import randint, shuffle
from ast import literal_eval
from qs import questions, names, emolist,emoanswers, itemlabels
from slist import subjects, keycodes
import getdims
import math

myform=cgi.FieldStorage()
cgitb.enable()
cursor = MySQLdb.connect(host="localhost",user="askerry",passwd="password",db="aesbehave").cursor()
print 'Content-type:text/html\n\n'
dimfile='appraisals.csv'
[minindex,midindex,maxindex,Qindex,qlabelindex,qnumindex,dimdata,numdims]=getdims.extractdims(dimfile)


#cgitb.enable(display=0, logdir="/path/to/logdir")
print '''
<style type="text/css">
    body {
        font-family:verdana,arial,helvetica,sans-serif;
        font-size:100%;
    }
</style>
'''
#testing
theids=myform.keys()
subjid = myform['subjid'].value
match=0
if subjid in subjects: 
	subjindex=subjects.index(subjid)
	match=1
	keycode=keycodes[subjindex]
      	questionID=subjid[subjid.index('q'):subjid.index('q')+3]
      	qnum=int(questionID[1:])-1
else: 
	match=0
if match==0:	
	print "<center><br><br> OOPS:<br>"
	print "The subject ID you have provided is incorrect. Please return to the previous page and re-enter the subject ID provided on your Mechanical Turk start page."
else:
        #print "your id is correct <br>"
      	dnums=eval(myform['dnums'].value)
      	qindex=myform['qindex'].value
      	qindex=int(qindex)+1
      	dnum=dnums[qindex-1]
	totalqpersubj=len(dnums)
      	thisdim=dimdata[dnum-1]
	mintag=thisdim[minindex]
      	midtag=thisdim[midindex]
      	maxtag=thisdim[maxindex]
      	dlabel=thisdim[qlabelindex]
      	dquest=thisdim[Qindex]
      	question=questions[qnum]
	emoans=emoanswers[qnum]
	qname=names[qindex-1]
      	dquest=dquest.replace('NAMEVAR', qname)
	itemlabel=itemlabels[qnum]
      	print itemlabel
      	print questionID
      	question=question.replace('NAMEVAR', qname)
      	qindex=str(qindex)
      	dnumlist=str(dnums)
        if int(qindex)==1:
       		#add the person to the database:  "insert" command for new rows
       		cursor.execute('insert into NDE_dims (subjid) values (%s)',str(subjid))
       		formindex=cursor.execute("SELECT MAX(rownum) AS formindex FROM NDE_dims")
       		formindex = cursor.fetchone()
       		#print "<p> %s </p>" % (formindex)
       		thisvar=str(formindex)
       		thisvar=thisvar[1:-3]
       		formindex=thisvar
       		#print "<p> type: %s </p>" % thisvar
        else:
       		lastQ=str(dnums[int(qindex)-2])
       		keycode=myform['keycode'].value
                formindex=myform['rownum'].value
       		lastresponse=myform['response'].value
                lastitem=myform['item'].value
       		lastanswer=myform['correctans'].value
                lastdim=myform['dlabel'].value
		qvardim=lastdim
		qvaremo=lastdim+'_qemo'
       		qvaritem=lastdim+'_qlabel'
       		sql='update NDE_dims set ' +qvardim +' ="'+lastresponse+'" where rownum="'+formindex+'"'
       		cursor.execute(sql)
       		sql='update NDE_dims set ' +qvaritem +' ="'+lastitem+'" where rownum="'+formindex+'"'
       		cursor.execute(sql)
       		sql='update NDE_dims set ' +qvaremo +' ="'+lastanswer+'" where rownum="'+formindex+'"'
       		cursor.execute(sql)
        ### css setup
        print '''
        <head><title>Research Study</title>
        
        <body>
        <link rel="shortcut icon" href="favicon.ico" type="image/x-icon" />
        <style type="text/css" media="all">@import "css/drupalit.css";</style>
        <style type="text/css" media="all">@import "css/content.css";</style>
        <style type="text/css" media="all">@import "css/node.css";</style>
        <style type="text/css" media="all">@import "css/defaults.css";</style>
        <style type="text/css" media="all">@import "css/system.css";</style>
        <style type="text/css" media="all">@import "css/userhttp://htmledit.squarefree.com/.css";</style>
        <style type="text/css" media="all">@import "css/fieldgroup.css";</styl<style type="text/css" media="all">@import
        
        "css/date.css";</style>
        <style type="text/css" media="all">@import "css/acidfree.css";</style>
        <style type="text/css" media="all">@import "css/style.css";</style>
        <style type="text/css" media="all">
	.radioLeft{
    		text-align: center;
		display:inline-block;	
	}
	.questiondiv {
	  height:105px; width:75%; 
	  color:white;
	  //border-color:maroon; 
	  //border-style:solid; 
	  //border-width:1px; 
	  //float:left; 
	  background-color:#4852B7
	}
	.dimdiv {
          height:60px; width:75%;
          color:white;
          //border-color:maroon;
          //border-style:solid;
          //border-width:1px;
          //float:left;
          background-color:#483D8B
        }
	.label { 		 
		 margin-left: 15px;
		 margin-right: 15px;

	}
	</style>
        </head>
	'''
        ####end of setup
	nextthing='question.py'
        if int(qindex)<totalqpersubj:
		nextthing='question.py'
	else:
		nextthing='demographics.py'       	
	#print "main loop"
       	print '<center><b>Question %s/%s:</b><br><br>' % (qindex, totalqpersubj)
       	print '<div class=questiondiv><center>%s <br><br></div>' % (question)
	print '<div class=dimdiv><center><br>%s</div>' %(dquest)
	print '<div id="page_content" align="center"><form name="myform" action="%s" method="submit"o></div>'%(nextthing)
	def make_checkarray(emotionlist):
		numemos=len(emotionlist)
		#numcols=math.floor(math.sqrt(numemos))
		if numemos<4:
			numcols=numemos
		else:
			numcols=math.floor(math.sqrt(len(emolist)))
		numcols=4 #this will be prettier for this one
		buckets=[[] for i in range(0,numcols)]
		for n, emo in enumerate(emotionlist):
			col=int(n%numcols)
			emostring='<br><input type="radio" name="response" value="%s"><label for="%s">%s</label>' % (emo,emo,emo)
			buckets[col].append(emostring)
		mainprintout=[]
		for c in buckets:
			print '<div class="radioLeft" align="center">'
			for e in c:
				print e
			print '</div>'
	if dquest!='How is mary feeling':
		#print 'hello'
		print '(please use the following scale: 0=<b>'+mintag+'</b>, 5=<b>'+midtag+'</b>, 10=<b>'+maxtag+'</b>)' 
		print '<div style="padding: 10px;">%s<input style="width:500px;" type="range" name="response" value="5" min="0" max="10" step="1" id="slider1"/>%s</div>'%(mintag,maxtag)
	else:
		make_checkarray(emolist)
	
	print '''
	<br><br>
        <input type="hidden" name="subjid" value="'''+subjid+'''">
	<input type="hidden" name="item" value="'''+itemlabel+'''">
	<input type="hidden" name="correctans" value="'''+emoans+'''">
        <input type="hidden" name="keycode" value="'''+keycode+'''">       	
        <input type="hidden" name="qindex" value="'''+qindex+'''">
        <input type="hidden" name="dnums" value="'''+dnumlist+'''"> 
        <input type="hidden" name="rownum" value="'''+formindex+'''"> 	
        <input type="hidden" name="dlabel" value="'''+dlabel+'''"> 	
        <input type="submit" value="Continue" /></center>
        <br><br><br><br>
        </form>
        </div>
        </body>
        </html>
        '''
        
        #end

