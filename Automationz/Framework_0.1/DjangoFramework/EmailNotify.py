def Send_Email(Reciever, Subject, Objective, Body=None , type=None):
    from mailer import Mailer
    from mailer import Message

    #server.ehlo()
    #server.starttls()
               
    ToAddr = Reciever
    message = Message(From="AutomationReport@automationsolutionz.com",
                     To=ToAddr,
                     charset="utf-8")

   
    message.Subject = Subject + " - Test Deployment"
    message.Html = """<div id=":1ox" class="ii gt m146ced87dfe81da1 adP adO">
        <div id=":1np" class="a3s" style="overflow: hidden;">
        <div>
        <div style="border:solid 1px #dfdfdf;color:#686868;font:13px Arial;max-width:638px">
        <div style="padding:0 20px;background-color:#f5f5f5"><span style="vertical-align:middle">
        <img src="http://i.imgur.com/BqzPRSr.png" style="padding:6px;padding-top:12px;padding-left:1px;border-style:none"></span>
        </div>
        <div style="padding:20px;min-height:140px"><img style="min-height:128px;width:128px;vertical-align:top;float:left;padding-right:15px;margin:1px;margin-bottom:15px" src="http://i.imgur.com/GJfLPHI.png" class="">
        <span style="color:#686868;margin-top:2px;padding-bottom:6px"><p style="font-size:18px">Deployed Run-ID: %s </br> Run Objective: %s</p>
        </br><p><a style="display:inline-block;padding:7px 15px;margin-right:10px;background-color:#d44b38;color:#fff;font-size:15px;font-weight:bold;border:solid 1px #c43b28;white-space:normal;text-decoration:none" href="http://135.23.123.67:8080/Home/RunID/%s/" target="_blank">Open RunID Detail</a></p>
        </span>
        </div>
        <div style="border-top:solid 1px #dfdfdf;color:#636363;font:11px Arial;line-height:1.5em;padding:3px 20px;background-color:#f5f5f5">&copy Automation Solutionz, 1212 Countrystone Drive, Kitchener, N2N 3R4. 
        <br>You are receiving this notification because of being in the mailing list of the deployed test. 
        </div>
        </div>
        </div>
        </div>""" % (Subject, Objective, Subject)
    #Body = "Deployed Run-ID: " + Subject + "<br/>" + "Run Objective: " + Objective + "<br/>"
    #link = "<a href='135.23.123.67:8080/Home/RunID/'" + Subject + ">" +Subject + "</a>"
    #message.Html = message.Html + Body + "<br/>" + "<br/>"
    username = "AutomationReport@automationsolutionz.com"
    password = "te@mWork"

    sender = Mailer('smtp.automationsolutionz.com','25', True, username, password)
    sender.send(message)