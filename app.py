from flask import Flask
# Import all of our views
from application.views.index import index_page
from application.views.login import login_page
from application.views.register import register_page 
from application.views.dashboard import dashboard_page 
from application.views.help import help_page 
from application.views.settings import settings_page 
from application.views.table_template import table_template_page 
from application.views.order import order_form

from application.utils import SECRET

app = Flask(__name__, static_folder="application/static")
app.debug = False 
app.secret_key = SECRET

# Register our views
app.register_blueprint(index_page)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(dashboard_page)
app.register_blueprint(help_page)
app.register_blueprint(settings_page)
app.register_blueprint(table_template_page)
app.register_blueprint(order_form)

if __name__ == '__main__':
    import application.database 
    app.run()

