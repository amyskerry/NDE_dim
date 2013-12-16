#!/usr/bin/python

import cgitb, cgi, MySQLdb, ast
#import cgitb, cgi, ast
import cPickle as p
from random import randint, shuffle
from ast import literal_eval
from qs import emoanswers

myform=cgi.FieldStorage()
cgitb.enable()
cursor = MySQLdb.connect(host="localhost",user="askerry",passwd="password",db="aesbehave").cursor()
print 'Content-type:text/html\n\n'

print '''
<style type="text/css">
    body {
        font-family:verdana,arial,helvetica,sans-serif;
        font-size:100%;
    }
</style>
'''

#cgitb.enable(display=0, logdir="/path/to/logdir")
theids=myform.keys() 
subjid = myform['subjid'].value
questionID=subjid[subjid.index('q'):subjid.index('q')+3]
qnum=int(questionID[1:])-1 
qindex=myform['qindex'].value
dnums=myform['dnums'].value
keycode=myform['keycode'].value
dnums=eval(dnums)
qindex=int(qindex)+1
emoans=emoanswers[qnum]
#print "<p>these are the ids: %s </p>" %(theids)
herresponse=myform['response'].value
#print "<p>previous response: %s </p>" %(herresponse)

lastQ=str(dnums[int(qindex)-2])
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
<head><title>Research Study: Demographics</title>

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
<style>
  .pagealign{
                text-align:left;
                margin-left:130px;margin-right:20px

        }	
  .demoalign{
        }
        label {
                 margin-left: 0px;
                 margin-right: 10px;
        }

</style>

<script type="text/javascript">
function validate(form){
    if (!checkTextField(form.gender)) {alert('Please enter your gender!');return false;}
    if (!checkTextField(form.age)) {alert('Please enter your age!');return false;}
    return true;
}
function checkRadioArray(radioButtons){
    for (var i=0; i< radioButtons.length; i++) {
        if (radioButtons[i].checked) return true;
    }
    return false;
}
function checkTextField(textField){
    if (textField.value!='') return true;
    return false;
}
</script>
</head>
'''
####end of setup

print '''
<div id="page_content" style="margin-right:160px;  margin-left: 160px;">

<p style="text-align:center"><font size="5"> Demographics </font></p>
<br>
<p style="text-align:center">Thank you for completing our study! We have a few quick follow up questions for you.</p>
<br><br>
<form name="myform" action="debrief.py" method="submit" onSubmit="return validate(myform)">
<div class=pagealign> 
Please tell us where you are from.
<br>
<label for="city">City (optional): </label> <input type="text" name="city" size=30>
<br>
<label for="country" >Country (optional): </label><input type="text" name="country" size=30>
<br><br>
<label for="gender" >Gender: </label><input type="text" name="gender" size=30>
<br>
<label for="age">Age: </label><input type="text" name="age" size=30>
<br><br>
</table><br>
Do you have any comments, thoughts, or feedback about this study? 
<br><textarea name="thoughts" cols=80 rows=5> </textarea><br>
</div>
<br><br><br>
<center>
We very much appreciate you taking the time to do this study.<br>
When you click continue you will receive a code that allows you to <b> recieve your payment.<center>
<br><br>
<input type="hidden" name="subjid" value="'''+subjid+'''">
<input type="hidden" name="keycode" value="'''+keycode+'''"> 
<input type="hidden" name="rownum" value="'''+formindex+'''"> 
<input type="submit" value="Continue" /></center>
<br><br><br><br>
</form>
</div>
</body>
</html>
'''
#end
