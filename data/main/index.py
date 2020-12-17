from flask import Blueprint, render_template, request, session

main_blue = Blueprint('main_blue', __name__)

@main_blue.route('/')
def index() :
    data = {'confirmator' : 204, 'heal' : 17, 'die':2}
    html = render_template('index.html', data = data)
    return html
