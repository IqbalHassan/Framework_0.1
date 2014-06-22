def Send_Email(Reciever, Subject, Body=None , type=None):
    from mailer import Mailer
    from mailer import Message

    #server.ehlo()
    #server.starttls()
               
    ToAddr = Reciever
    message = Message(From="AutomationReport@automationsolutionz.com",
                     To=ToAddr,
                     charset="utf-8")

   
    message.Subject = Subject
    message.Html = "<strong> Run <br/> <strong>"
    Body = "Assigned Task: "
    link = "<a href='135.23.123.67:8080/Home/RunID/'" + Subject + ">" +Subject + "</a>"
    message.Html = message.Html + Body + Subject + "<br/>" + link
    username = "AutomationReport@automationsolutionz.com"
    password = "te@mWork"

    sender = Mailer('smtp.automationsolutionz.com','25', True, username, password)
    sender.send(message)