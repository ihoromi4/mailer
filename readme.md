# Python 3 Mailer

This script sends the same message to a list of e-mail addresses. It uses html-formated messages so one can add images and CSS styles. 

## Dependencies

* python >= 3.4
* smtplib

## Emails List

File `emails.txt` contains e-mails list: each address is on a new line.

```
example_email@gmail.com
another_email@gmail.com
...
...
...
100500_email.@gmail.com
```

## Mailer Configuration

File `config.json` contains json-encoded configuration for mailer script.

```json
{
    "server_url": "smtp.gmail.com:587",
    "account": {
        "user": "test_user",
        "password": "test_password"
    },
    "emails_file": "emails.txt",
    "message": {
        "file": "message.html",
        "subject": "Subject",
        "from": "From"
    },
    "timeout": 40
}
```

## Message Format

File `message.html` contains html-formated message. For example:

```html
<html>
    <body>
        <h1>Example message</h1>
        <p>Message text</p>
    </body>
</html>
```

## Errors And Logging

Error reports are saved to `mail.log`.

## Google Gmail Support

To send message from `Google Gmail` account you need to do several actions.

Firstly, go to [less secure app access](https://www.google.com/settings/security/lesssecureapps) page and enable toggle.

Then you must try to run script. Your attempt ends with access denied report. Then you should go to e-mail box and confirm access for less secure application from your PC.
