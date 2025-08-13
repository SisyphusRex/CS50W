//TODO: Fix css file so the elements will use style

document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    // listen for compose email send submit
    document.querySelector('#compose-form').onsubmit = () => send_email();

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email(emailToReplyTo = 'none') {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#single-email-view').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

    if (emailToReplyTo !== 'none') {
        document.querySelector('#compose-recipients').value = emailToReplyTo.sender;
        var subject = 'Re: ';
        subject += emailToReplyTo.subject;
        document.querySelector('#compose-subject').value = subject;
        var body = `On ${emailToReplyTo.timestamp} ${emailToReplyTo.sender} wrote: ${emailToReplyTo.body}`;

    }
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#single-email-view').style.display = 'none';

    document.querySelector('#emails')

    // Show the mailbox name

    document.querySelector('#mailbox-title').textContent = `${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}`;

    document.querySelector('#email-divs').innerHTML = '';

    // query email server
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            console.log(emails);
            if (emails.error) {

            } else {
                for (let email of emails) {

                    var newDiv = document.createElement('div');
                    newDiv.style.border = '1px solid blue';
                    newDiv.style.marginBottom = '5px';
                    if (email.read === 'true') {
                        newDiv.style.backgroundColor = 'grey';
                    } else {
                        newDiv.style.backgroundColor = 'green';
                    }
                    var fromAddress = document.createElement('span');
                    fromAddress.style.padding = '10px';
                    fromAddress.style.fontWeight = 'bold';
                    var subject = document.createElement('span');
                    subject.style.padding = '10px';
                    var timeStamp = document.createElement('span');
                    timeStamp.style.float = 'right';
                    fromAddress.textContent = email.sender;
                    subject.textContent = email.subject;
                    timeStamp.textContent = email.timestamp;

                    newDiv.append(fromAddress, subject, timeStamp);

                    newDiv.addEventListener('click', () => load_email(email.id));

                    document.querySelector('#email-divs').appendChild(newDiv);
                }
            }
        })
        .catch(error => {
            console.log(error.message);
        })

    return false;
}

function send_email() {
    // make a post with email info

    // get email info from form
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    // send post
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.error) {

            } else {
                load_mailbox('sent');
            }
        })
        .catch(error => {
            console.log(error.message);
        })

    // return to inbox after send
    return false;
}

function load_email(emailID) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#single-email-view').style.display = 'block';

    fetch(`/emails/${emailID}`)
        .then(response => response.json())
        .then(data => {
            const from = document.createElement('span');
            const to = document.createElement('span');
            const subject = document.createElement('span');
            const timeStamp = document.createElement('span');
            const body = document.createElement('p');

            from.textContent = data.sender;
            for (let address of data.recipients) {
                to.textContent += `${address}, `;
            }
            subject.textContent = data.subject;
            timeStamp.textContent = data.timestamp;
            body.textContent = data.body;



            document.querySelector('#from-div').appendChild(from);
            document.querySelector('#to-div').appendChild(to);
            document.querySelector('#subject-div').appendChild(subject);
            document.querySelector('#timestamp-div').appendChild(timeStamp);
            document.querySelector('#email-body').appendChild(body);

            const replyButton = document.createElement('button');
            replyButton.className = 'btn btn-sm btn-outline-primary';
            replyButton.innerHTML = 'Reply';
            replyButton.addEventListener('click', () => compose_email(data));
            document.querySelector('#reply').appendChild(replyButton);

        })

    return false;
}
