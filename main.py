from flask import Flask, render_template, request, url_for, redirect
import sqlite3 as sql
import datetime as dt

app = Flask(__name__)

DomQuery = '''SELECT * FROM flights WHERE DATE = ? '''
InterQuery = '''SELECT * FROM flights WHERE ID <= ? '''


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/pred', methods=['POST', 'GET'])
def pred():
    try:
        if request.method == 'POST':
            date = request.form['date']
            date = dt.datetime.strptime(date, '%Y-%m-%d').date()
            day = date.day

            flight = request.form['optradio']

            with sql.connect('fare.db') as con:
                cur = con.cursor()

                cur.execute(DomQuery, (date,))
                row = cur.fetchall()

                cur.execute(InterQuery, (row[0][0],))
                allRow = cur.fetchall()
                print(allRow)

    except(Exception)as e:
        print(e)
        return render_template('index.html', Hello="Please Select Flight and Date")
    else:
        if(flight == 'Domestic'):
            return render_template('index.html', Hello='Avg Total Flight fare on\t{0} is\t{1}'.format(row[0][1], row[0][2]), TableValues=allRow, flight='Domestic')
        else:
            return render_template('index.html', Hello='Avg Total Flight fare on\t{0} is\t{1}'.format(row[0][1], row[0][3]), TableValues=allRow, flight='International')
    finally:
        con.close()


if __name__ == '__main__':
    app.run(debug=True)

# <button class="btn btn--radius btn--green" type="submit" name="inter">International</button>
