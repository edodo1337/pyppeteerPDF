from flask import Flask, jsonify, abort, make_response, request
from flask import render_template, flash, redirect, url_for
#from flask_wtf import FlaskForm
#from flask_restplus import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint
#from flask_swagger import swagger
#from wtforms import StringField, PasswordField, BooleanField, SubmitField
#from pyppeteer import launch
from flask_restplus import Resource, Api
from pyppe import html_to_pdf
import asyncio
#import json




app = Flask(__name__)
api = Api(app, version='1.0', title='Sample API',
    description='A sample API')

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yml'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "HTML to PDF"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.config['SECRET_KEY'] = '123'

# model = api.model('Name Model',
# 		  {'path_page': fields.String(required = True,
# 					 description="Page URL",
# 					 help="")})







@app.route('/', methods=['GET', 'POST'])
def index():
    form = InterfaceForm()
    if form.validate_on_submit():
        flash('Path is: {}'.format(
            form.path.data))
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio.get_event_loop().run_until_complete(html_to_pdf(form.path.data))
            flash('Done')
            return redirect('/')
        except:
            form.path.data = None
            flash('Error')
    return render_template('index.html', form=form)


@app.route('/api/', methods=['GET', 'POST'])
def get():
    print(request.args['url'])
    #print(req)

    try:
        path_page = request.args['url']
        #path_page = "http://" + path_page
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(html_to_pdf(path_page))
        return {
            "status": "Done"
        }
    except:
        abort(make_response(jsonify(status="Bad request"), 400))
        return {
            "status": "Error"
        }






if __name__=='__main__':
    app.run(debug=True)