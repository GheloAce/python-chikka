
# Python Chikka #

## Installation ##

    $ pip install python-chikka

## Usage ##

    from chikka import Chikka

    c = Chikka(client_id=CLIENT_ID, secret_key=SECRET_KEY, shortcode=SHORTCODE)
    c.send('09991234567', 'Mensahe mo')

Before sending your message you may  define a message_id
if you do not supply a message_id a random message_id will
be generated.

    c.send('09991234567', 'Mensahe mo na may message id', message_id='1234567890')

## Testing ##

Unit tested for:

* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5

