import smtplib
import urlparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def Send_Email(Receiver, Subject, Objective, Tester, StartDate, EndDate, EstimatedTime, Body=None , type=None):
    
    current_url = self.request.url
    print current_url
    current_url = urlparse.urlparse(current_url).hostname
    
    ToAddr = Receiver
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Subject + " - Test Deployment"
    msg['From'] = "automation.solutionz@gmail.com"
    msg['To'] = ToAddr
    
    html = """<div id=":1ox" class="ii gt m146ced87dfe81da1 adP adO">
        <div id=":1np" class="a3s" style="overflow: hidden;">
        <div>
        <div style="border:solid 1px #dfdfdf;color:#686868;font:13px Arial;max-width:638px">
        <div style="padding:0 20px;background-color:#f5f5f5"><span style="vertical-align:middle">
        <img src="http://i.imgur.com/BqzPRSr.png" style="padding:6px;padding-top:12px;padding-left:1px;border-style:none"></span>
        </div>
        <div style="padding:20px;min-height:140px"><img style="min-height:128px;width:128px;vertical-align:top;float:left;padding-right:15px;margin:1px;margin-bottom:15px" src="http://i.imgur.com/GJfLPHI.png" class="">
        <span style="color:#686868;margin-top:2px;padding-bottom:6px"><p style="font-size:18px">Deployed Run-ID: %s </p><p style="font-size:18px">  Run Objective: %s</p>
        <p><a style="display:inline-block;padding:7px 15px;margin-right:10px;background-color:#d44b38;color:#fff;font-size:15px;font-weight:bold;border:solid 1px #c43b28;white-space:normal;text-decoration:none" href="http://%s/Home/RunID/%s/" target="_blank">Open RunID Detail</a></p>
        </span>
        <br/>
        
        <table style="border: solid #ccc 1px;-moz-border-radius: 6px;-webkit-border-radius: 6px;border-radius: 6px;-webkit-box-shadow: 0 1px 1px #ccc; -moz-box-shadow: 0 1px 1px #ccc; box-shadow: 0 1px 1px #ccc;">
        <thead>
        <tr>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5); -moz-border-radius: 6px 0 0 0;-webkit-border-radius: 6px 0 0 0;border-radius: 6px 0 0 0;">Run ID</th>        
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);">Objective</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);">Status</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);">Tester</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);">Start Date</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);">End Date</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);-moz-border-radius: 0 6px 0 0;-webkit-border-radius: 0 6px 0 0;border-radius: 0 6px 0 0;">Estimated Time</th>
        </tr>
        </thead>
        <tr>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;-moz-border-radius: 0 0 0 6px;-webkit-border-radius: 0 0 0 6px;border-radius: 0 0 0 6px;">%s</td>        
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;-moz-border-radius: 0 0 6px 0;-webkit-border-radius: 0 0 6px 0;border-radius: 0 0 6px 0;">%s</td>
        </tr>        
        </table>
        
        </div>
        
        <div style="border-top:solid 1px #dfdfdf;color:#636363;font:11px Arial;line-height:1.5em;padding:3px 20px;background-color:#f5f5f5">&copy; Automation Solutionz, 1212 Countrystone Drive, Kitchener, N2N 3R4. 
        <br>You are receiving this notification because of being in the mailing list of the deployed test. 
        </div>
        </div>
        </div>
        </div>""" % (Subject, Objective, current_url, Subject, Subject, Objective, 'Submitted', Tester, StartDate, EndDate, EstimatedTime)
    
    part2 = MIMEText(html, 'html')
    
    msg.attach(part2)
    
    
    username = "automation.solutionz@gmail.com"
    password = "te@mWork"

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail('automation.solutionz@gmail.com',Receiver,msg.as_string())
    server.close()
    
    
def Complete_Email(self, Receiver, Subject, Objective, Status, List, Tester,Duration, Body=None , type=None):
    from mailer import Mailer
    from mailer import Message

    
    from pygooglechart import PieChart2D
    
    current_url = self.request.url
    print current_url

    chart = PieChart2D(550, 400)
    
    chart.set_colours(['82D434','FD363B','FFA639','1F1FFF','5E5E5E','88A388'])
    chart.add_data([List[0], List[1], List[2], List[3], List[4], List[5]])
    
    chart.set_pie_labels(['Passed', 'Failed', 'Blocked', 'In-Progress', 'Submitted', 'Skipped'])
    
    print chart.get_url()
    
    chart.download('pie-hello-world.png')
    
                          
    ToAddr = Receiver
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Subject + " - Test Deployment"
    msg['From'] = "automation.solutionz@gmail.com"
    msg['To'] = ToAddr
    
    html = """<div id=":1ox" class="ii gt m146ced87dfe81da1 adP adO">
        <div id=":1np" class="a3s" style="overflow: hidden;">
        <div>
        <div style="border:solid 1px #dfdfdf;color:#686868;font:13px Arial;max-width:650px">
        <div style="padding:0 20px;background-color:#f5f5f5"><span style="vertical-align:middle">
        <img src="http://i.imgur.com/BqzPRSr.png" style="padding:6px;padding-top:12px;padding-left:1px;border-style:none"></span>
        </div>
        <div style="padding:20px;min-height:550px;min-width:600px"><img style="min-height:128px;width:128px;vertical-align:top;float:left;padding-right:15px;margin:1px;margin-bottom:15px" src="http://i.imgur.com/GJfLPHI.png" class="">
        <span style="color:#686868;margin-top:2px;padding-bottom:6px"><p style="font-size:18px">Deployed Run-ID: %s </p><p style="font-size:18px">  Run Objective: %s</p><p style="font-size:18px">  Run Status: %s</p>
        <img src="%s" class="">
        <h2>Execution Summary</h2>
        <table style="border: solid #ccc 1px;-moz-border-radius: 6px;-webkit-border-radius: 6px;border-radius: 6px;-webkit-box-shadow: 0 1px 1px #ccc; -moz-box-shadow: 0 1px 1px #ccc; box-shadow: 0 1px 1px #ccc;">
        <thead>
        <tr>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5); -moz-border-radius: 6px 0 0 0;-webkit-border-radius: 6px 0 0 0;border-radius: 6px 0 0 0;"><div style="width:15px;height:10px;border:1px solid grey;background-color:#82D434"></div>Passed</th>        
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);"><div style="width:15px;height:10px;border:1px solid grey;background-color:#FD363B"></div>Failed</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);"><div style="width:15px;height:10px;border:1px solid grey;background-color:#FFA639"></div>Blocked</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);"><div style="width:15px;height:10px;border:1px solid grey;background-color:#1F1FFF"></div>In-Progress</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);"><div style="width:15px;height:10px;border:1px solid grey;background-color:#5E5E5E"></div>Submitted</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);"><div style="width:15px;height:10px;border:1px solid grey;background-color:#88A388"></div>Skipped</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);-moz-border-radius: 0 6px 0 0;-webkit-border-radius: 0 6px 0 0;border-radius: 0 6px 0 0;">Total Cases</th>
        </tr>
        </thead>
        <tr>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;-moz-border-radius: 0 0 0 6px;-webkit-border-radius: 0 0 0 6px;border-radius: 0 0 0 6px;">%s</td>        
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;-moz-border-radius: 0 0 6px 0;-webkit-border-radius: 0 0 6px 0;border-radius: 0 0 6px 0;">%s</td>
        </tr>        
        </table>
        </br>
        <table style="border: solid #ccc 1px;-moz-border-radius: 6px;-webkit-border-radius: 6px;border-radius: 6px;-webkit-box-shadow: 0 1px 1px #ccc; -moz-box-shadow: 0 1px 1px #ccc; box-shadow: 0 1px 1px #ccc;">
        <thead>
        <tr>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5); -moz-border-radius: 6px 0 0 0;-webkit-border-radius: 6px 0 0 0;border-radius: 6px 0 0 0;">Run ID</th>        
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);">Objective</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);">Status</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);">Tester</th>
        <th style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;background-color: #dce9f9; background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);background-image:         linear-gradient(top, #ebf3fc, #dce9f9);-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset; -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset; box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;border-top: none;text-shadow: 0 1px 0 rgba(255,255,255,.5);-moz-border-radius: 0 6px 0 0;-webkit-border-radius: 0 6px 0 0;border-radius: 0 6px 0 0;">Execution Time</th>
        </tr>
        </thead>
        <tr>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;-moz-border-radius: 0 0 0 6px;-webkit-border-radius: 0 0 0 6px;border-radius: 0 0 0 6px;">%s</td>        
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;">%s</td>
        <td style="border-left: 1px solid #ccc;border-top: 1px solid #ccc;padding: 10px;text-align: left;-moz-border-radius: 0 0 6px 0;-webkit-border-radius: 0 0 6px 0;border-radius: 0 0 6px 0;">%s</td>
        </tr>        
        </table>
        
        <p><a style="display:inline-block;padding:7px 15px;margin-right:10px;background-color:#d44b38;color:#fff;font-size:15px;font-weight:bold;border:solid 1px #c43b28;white-space:normal;text-decoration:none" href="http://%s/Home/RunID/%s/" target="_blank">View Full Report</a></p>        
        </span>
        </div>
        <div style="border-top:solid 1px #dfdfdf;color:#636363;font:11px Arial;line-height:1.5em;padding:3px 20px;background-color:#f5f5f5">&copy; Automation Solutionz, 1212 Countrystone Drive, Kitchener, N2N 3R4. 
        <br>You are receiving this notification because of being in the mailing list of the deployed test. 
        </div>
        </div>
        </div>
        </div>""" % (Subject, Objective, Status, chart.get_url(), List[0],List[1],List[2],List[3],List[4],List[5],List[6],Subject,Objective, Status,Tester[0],Duration[0], current_url, Subject)
    
    part2 = MIMEText(html, 'html')
    
    msg.attach(part2)
    
    
    username = "automation.solutionz@gmail.com"
    password = "te@mWork"

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail('automation.solutionz@gmail.com',Receiver,msg.as_string())
    server.close()
    
    
    
