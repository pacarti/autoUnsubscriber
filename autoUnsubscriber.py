import imapclient, pyzmail, webbrowser, bs4, getpass

emailAddress = input("Your e-mail address: ")
pwd = getpass.getpass("Your e-mail password: ")
unsubscribeKeywords = ['rezygn', 'Rezygn', 'subskrybcj', 'Subskrypcj', 'wypis', 'Wypis', 'powiadom', 'nie otrzymy', 'unsubscribe', 'Unsubscribe']

imapObj = imapclient.IMAPClient('[your email IMAP server]', 993)

imapObj.login(emailAddress, pwd)

imapObj.select_folder('INBOX', readonly=True)

UIDs = imapObj.search('ALL')


for UID in UIDs:
    rawMessage = imapObj.fetch([UID], ['BODY[]', 'FLAGS'])
    rawMessageBody = pyzmail.PyzMessage.factory(rawMessage[UID][b'BODY[]'])
    try:
        messageHTML = rawMessageBody.html_part.get_payload().decode('UTF-8')
        soup = bs4.BeautifulSoup(messageHTML, 'html.parser')
        aElems = soup.select('a')
        for a in aElems:
            linkText = a.getText()
            for keyword in unsubscribeKeywords:
                if keyword in linkText:
                    unsubscribeLink = a.get('href')
                    webbrowser.open(unsubscribeLink)
    except AttributeError:
        continue
