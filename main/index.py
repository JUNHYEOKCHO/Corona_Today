from flask import Blueprint, render_template, request, session

main_blue = Blueprint('main_blue', __name__)

@main_blue.route('/index')
def index() :
    data = {'confirmator' : 20842, 'heal' : 15783, 'die':331}
    html = render_template('index.html', data = data)
    return html


@main_blue.route('/')
def protection_search() :
    data = {'confirmator' : 20842, 'heal' : 15783, 'die':331}
    html = render_template('index.html', data = data)
    return html

@main_blue.route('/robots.txt')
def robots() :
    
    html = render_template('robots.txt')
    return html

@main_blue.route('/sitemap.xml')
def sitemap() :
    
    html = render_template('sitemap.xml')
    return html