from flask import Flask, render_template, request, redirect, url_for, flash
import asyncio

import db
import wiz

loop = asyncio.get_event_loop()
app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    db.close_db()


@app.route("/scan")
def scan():
    try:
        loop.run_until_complete(wiz.scan())
    except Exception as error:
        flash(f'Scan: {error}', 'warning')

    return redirect(url_for("index"))


@app.route("/on/<string:ip>")
def on(ip):
    try:
        if ip == 'all':
            bulbs = db.get_online_bulbs()
            for bulb in bulbs:
                loop.run_until_complete(wiz.on(bulb["IP"]))
        else:
            loop.run_until_complete(wiz.on(ip))
    except Exception as error:
        flash(f'Bulb {ip}: {error}', 'warning')

    return redirect(url_for("index"))


@app.route("/off/<string:ip>")
def off(ip):
    try:
        if ip == 'all':
            bulbs = db.get_online_bulbs()
            for bulb in bulbs:
                loop.run_until_complete(wiz.off(bulb["IP"]))
        else:
            loop.run_until_complete(wiz.off(ip))
    except Exception as error:
        flash(f'Bulb {ip}: {error}', 'warning')

    return redirect(url_for("index"))


@app.route("/scene/<string:ip>/<int:no>")
def scene(ip, no):
    try:
        if ip == 'all':
            bulbs = db.get_online_bulbs()
            for bulb in bulbs:
                loop.run_until_complete(wiz.scene(bulb["IP"], no))
        else:
            loop.run_until_complete(wiz.scene(ip, no))
    except Exception as error:
        flash(f'Bulb {ip}: {error}', 'warning')

    return redirect(url_for("index"))


@app.route("/")
@app.route("/index")
def index():
    bulbs = db.get_all_bulbs()
    return render_template("index.html", bulbs=bulbs)


@app.route("/edit_bulb/<string:ip>", methods=['POST', 'GET'])
def edit_bulb(ip):
    if request.method == 'POST':
        # ip = request.form['ip']
        name = request.form['name']
        db.edit_bulb(ip, name)
        flash(f'Bulb {ip} - {name} updated', 'success')
        return redirect(url_for("index"))
    data = db.get_bulb(ip)
    return render_template("edit_bulb.html", bulb=data)


@app.route("/delete_bulb/<string:ip>")
def delete_bulb(ip):
    db.delete_bulb(ip)
    flash(f'Bulb {ip} deleted', 'warning')
    return redirect(url_for("index"))


if __name__ == '__main__':
    with app.app_context():
        db.init_db()
    app.secret_key = 'WiZfLaSk'
    app.run(host='0.0.0.0', port=8000, debug=True)
