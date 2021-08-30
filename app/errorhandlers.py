from flask import render_template
from enum import Enum

def page_not_found(e):
    return render_template('404.html'), 404


def method_not_allowed(e):
    return render_template('405.html'), 405


def internal_server_error(e):
    return render_template('500.html'), 500


def forbidden(e):
    return render_template('403.html'), 403



#Proxy data pattern

AppErrors = {
"PAGE_NOT_FOUND":404,
"METHOD_NOT_ALLOWED":405,
"INTERNAL_SERVER_ERROR":500,
"FORBIDDEN":403
}
def handle_error(e):
    return render_template(f'{AppErrors[e]}.html'),AppErrors[e]



