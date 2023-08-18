from flask import redirect
from app import app


@app.route('/author')
def author():
    return redirect('https://github.com/lyaguxafrog')
