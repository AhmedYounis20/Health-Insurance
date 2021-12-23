from flask import Flask
from flask import render_template



app=Flask(__name__,template_folder='../templates')



@app.route('/admin/')
def admin():
    return render_template('admin/dashboard.html')


app.run()