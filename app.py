# app.py is server file
# import email
import timeit
import re
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from matplotlib.pyplot import table
import yaml

app = Flask(__name__)

# configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)



@app.route('/')
def showtable():
    cur = mysql.connection.cursor()
    RESULT = cur.execute(
        "SHOW TABLES")
    # columns = cur.execute('show columns from civilians')
    if RESULT > 0:
        userDetails = cur.fetchall()
        return render_template("homePage.html", userDetails=userDetails)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    # getting the table name
    tablename = request.args.get('table')
    typeofquery = request.args.get('type')
    # return render_template('/debbug.html', tablename=tablename, t=typeofquery)
    cur = mysql.connection.cursor()

    cur.execute('SHOW COLUMNS FROM %s' % (tablename))
    columns = cur.fetchall()

    # cmnd = "insert into %s values ("
    # for i in range(len(columns)):
    #     cmnd += "%s,"
    # cmnd = cmnd[:len(cmnd)-1] + ");"

    if request.method == 'POST':
        # fetch form data

        userDetails = request.form

        cmnd = "INSERT INTO " + tablename + "("
        toAdd = [column[0] for column in columns]

        for i in range(len(toAdd)):
            if (i == len(toAdd)-1):
                cmnd += toAdd[i]
            else:
                cmnd += toAdd[i] + ", "

        cmnd = cmnd + ") VALUES ("
        # lst = ['%s']*len(toAdd)
        # lst = tuple(lst)

        # for i in range(len(toAdd)):
        #     if (i == len(toAdd)-1):
        #         cmnd += "%s"
        #     else:
        #         cmnd += "%s, "
        # cmnd = cmnd + ")"

        toAdd = []
        for i in userDetails:
            toAdd.append(userDetails[i])

        for i in range(len(toAdd)):
            if (i == len(toAdd)-1):
                cmnd += "'"+str(toAdd[i])+"'"
            else:
                cmnd += "'"+str(toAdd[i])+"', "
        cmnd = cmnd + ")"

        # toAdd = []
        # for i in userDetails:
        #     toAdd.append(userDetails[i])
        # print("the command is", cmnd)

        # print("the to add is ", toAdd)
        # mysql.connection.commit()
        # cur.close()
        # return render_template('/debug.html', toAdd=toAdd, cmnd=cmnd, columns=columns, userDetails=userDetails)
        # cur.execute(cmnd % tuple(toAdd))
        cur.execute(cmnd)
        cur.fetchall()

        mysql.connection.commit()
        cur.close()
        return render_template('/insertionSuccesful.html', t=typeofquery, tablename=tablename)

    return render_template('insert.html', columns=columns, t=typeofquery, tablename=tablename)


@ app.route('/users')
def users():
    # print(request.args.get('table')[:])
    # getting the table name
    tablename = request.args.get('table')[:]

    cur = mysql.connection.cursor()
    cur.execute('SHOW COLUMNS FROM %s' % (tablename))
    columns = cur.fetchall()
    RESULT = cur.execute(
        "SELECT * FROM  %s" % (tablename))
    if RESULT > 0:
        userDetails = cur.fetchall()
        return render_template("users.html", userDetails=userDetails, columns=columns)
    # else:
    #     return render_template("users.html", userDetails=userDetails)


@ app.route('/finish', methods=['GET', 'POST'])
def finish():
    return render_template('insertionSuccesful.html', t='a')


@ app.route('/delete', methods=['GET', 'POST'])
def delete():
    tablename = request.args.get('table')[:]
    typeofquery = request.args.get('type')[:]
    if request.method == 'POST':
        # fetch form data

        userDetails = request.form
        # ame = userDetails['name']
        # cur = mysql.connection.cursor()
        # cur.execute(
        #     "delete from %s where name= '%s' " % (tablename, name))
        # mysql.connection.commit()
        # cur.close()
        return render_template('/debug2.html', userDetails=userDetails, t=tablename, typeofquery=typeofquery)
    return render_template('delete.html', typeofquery=typeofquery, t=tablename)
    # return render_template('/debbug.html', typeofquery=typeofquery, t=tablename)


@ app.route('/updelete', methods=['GET', 'POST'])
def deleteup():
    if request.method == 'POST':
        # fetch form data
        tablename = request.args.get('table')[:]
        userDetails = request.form
        # ame = userDetails['name']
        # cur = mysql.connection.cursor()
        # cur.execute(
        #     "delete from %s where name= '%s' " % (tablename, name))
        # mysql.connection.commit()
        # cur.close()
        return render_template('/debug3.html', userDetails=userDetails, t=tablename)
    return render_template('updelete.html')


@ app.route('/delet3', methods=['GET', 'POST'])
def delete3():
    tablename = request.args.get('table')[:]
    rowNo = request.args.get('primaryKey')
    typeofquery = request.args.get('type')
    # return render_template('/debbug.html',tablename =?)
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form

        cur = mysql.connection.cursor()
        # cur.execute(
        #     "delete from %s where name= '%s' " % (tablename, name))\\
        cur.execute("select * from %s " % (tablename))
        tabledetails = cur.fetchall()

        if (rowNo.isnumeric() == False):
            # throw error
            errorr = 0
            return render_template('/errror.html')
        rowToBeDeleted = tabledetails[int(rowNo)-1]

        cur.execute('SHOW COLUMNS FROM %s' % (tablename))
        columns = cur.fetchall()

        cmnd = "delete from " + tablename + " where "
        toAdd = [column[0] for column in columns]

        for i in range(len(toAdd)):
            if (columns[i][1] == 'int'):
                if (i == len(toAdd)-1):
                    cmnd += str(toAdd[i]) + "= " + str(rowToBeDeleted[i])
                else:
                    cmnd += str(toAdd[i]) + "= " + \
                        str(rowToBeDeleted[i]) + " and "
            else:
                if (i == len(toAdd)-1):
                    cmnd += str(toAdd[i]) + "= " + " \"" + \
                        str(rowToBeDeleted[i]) + "\""
                else:
                    cmnd += str(toAdd[i]) + "= " + " \"" + \
                        str(rowToBeDeleted[i]) + "\"" + " and "
        cur.execute(cmnd)
        mysql.connection.commit()
        cur.close()
        return render_template('/insertionSuccesful.html', userDetails=userDetails, tablename=tablename, rowNo=rowNo, td=tabledetails, rtbd=rowToBeDeleted, cmnd=cmnd, columns=columns, t=typeofquery)
    return render_template('delet3.html')


@ app.route('/dele4', methods=['GET', 'POST'])
def delete4():
    tablename = request.args.get('table')[:]
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form
        rowNo = request.args.get('primaryKey')

        cur = mysql.connection.cursor()
        # cur.execute(
        #     "delete from %s where name= '%s' " % (tablename, name))\\
        cur.execute("select * from %s " % (tablename))
        tabledetails = cur.fetchall()

        if (rowNo.isnumeric() == False):
            # throw error
            errorr = 0
            return render_template('/errror.html')
        # return render_template('/debbug.html', a=tabledetails[0])
        rowToBeDeleted = tabledetails[int(rowNo)-1]

        cur.execute('SHOW COLUMNS FROM %s' % (tablename))
        columns = cur.fetchall()

        cmnd = "delete from " + tablename + " where "
        toAdd = [column[0] for column in columns]

        for i in range(len(toAdd)):
            if (columns[i][1] == 'int'):
                if (i == len(toAdd)-1):
                    cmnd += str(toAdd[i]) + "= " + str(rowToBeDeleted[i])
                else:
                    cmnd += str(toAdd[i]) + "= " + \
                        str(rowToBeDeleted[i]) + " and "
            else:
                if (i == len(toAdd)-1):
                    cmnd += str(toAdd[i]) + "= " + " \"" + \
                        str(rowToBeDeleted[i]) + "\""
                else:
                    cmnd += str(toAdd[i]) + "= " + " \"" + \
                        str(rowToBeDeleted[i]) + "\"" + " and "
        cur.execute(cmnd)
        mysql.connection.commit()
        cur.close()
        return redirect('insert?table=' + tablename, userDetails=userDetails, t=tablename, rowNo=rowNo, td=tabledetails, rtbd=rowToBeDeleted, cmnd=cmnd, columns=columns)
    return redirect('/insert?table=' + tablename)


@ app.route('/update', methods=['GET', 'POST'])
def update():
    tablename = request.args.get('table')[:]
    cur = mysql.connection.cursor()
    cur.execute('SHOW COLUMNS FROM %s' % (tablename))
    columns = cur.fetchall()
    if request.method == 'POST':

        cur = mysql.connection.cursor()

        userDetails = request.form

        # return redirect('/debug?primaryKey='+userDetails + '&table=' + tablename)
        return render_template('/debug2.html', userDetails=int(userDetails['primarykey']), t=tablename)
    return render_template('/update.html', columns=columns)


@ app.route('/update2', methods=['GET', 'POST'])
def update2():
    tablename = request.args.get('table')[:]
    print("printing request args")
    print(request.args.get)
    a = (request.args.get)
    cur = mysql.connection.cursor()
    cur.execute('SHOW COLUMNS FROM %s' % (tablename))
    columns = cur.fetchall()

    cur.execute('select * FROM %s' % (tablename))
    entry = cur.fetchall()

# delete
    userDetails = request.form
    rowNo = request.args.get('primaryKey')
    if (request.method == "POST"):

        cur = mysql.connection.cursor()

        cur.execute("select * from %s " % (tablename))
        tabledetails = cur.fetchall()

        if (rowNo.isnumeric() == False):
            # throw error
            return render_template('errror.html')
        rowToBeDeleted = tabledetails[int(rowNo)-1]

        cur.execute('SHOW COLUMNS FROM %s' % (tablename))
        columns = cur.fetchall()

        cmnd = "delete from " + tablename + " where "
        toAdd = [column[0] for column in columns]

        for i in range(len(toAdd)):
            if (columns[i][1] == 'int'):
                if (i == len(toAdd)-1):
                    cmnd += str(toAdd[i]) + "= " + str(rowToBeDeleted[i])
                else:
                    cmnd += str(toAdd[i]) + "= " + \
                        str(rowToBeDeleted[i]) + " and "
            else:
                if (i == len(toAdd)-1):
                    cmnd += str(toAdd[i]) + "= " + " \"" + \
                        str(rowToBeDeleted[i]) + "\""
                else:
                    cmnd += str(toAdd[i]) + "= " + " \"" + \
                        str(rowToBeDeleted[i]) + "\"" + " and "
        cur.execute(cmnd)
        mysql.connection.commit()
        cur.close()

        return render_template('/debug.html', aa=int(a('primaryKey'))-1, columns=columns, entry=entry)

    return render_template('update2.html', columns=columns)



@app.route('/assignment8', methods=['GET', 'POST'])
def assignment8():
    return render_template('assignment8.html')


@app.route('/assignment8/question1', methods=['GET', 'POST'])
def question1():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        prefix = request.form['prefix']
        suffix = request.form['suffix']
        
        query_prefix = prefix + "%"
        query_suffix = "%"+ suffix
        
        #Optimizied Query
        cur.execute("(select * from people where name_of_person like %s) union (select * from people where name_of_person like %s)", (query_prefix, query_suffix))
        mysql.connection.commit()
        output = cur.fetchall()

        return render_template('assignment8.html', data=output)

@app.route('/assignment8/question4', methods=['GET', 'POST'])
def question4():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        date_of_birth = request.form['date_of_birth']
        
        cur.execute("SELECT * FROM people WHERE date_of_birth=%s", [date_of_birth])
        mysql.connection.commit()

        output = cur.fetchall()

        return render_template('assignment8.html', data4=output)


@app.route('/assignment8/question5', methods=['GET', 'POST'])
def question5():
    if request.method == 'POST':
        cur = mysql.connection.cursor()

        cur.execute('select count(ifnull(qty_remaining,0)) from weapons')
        mysql.connection.commit()

        output = cur.fetchall()
        return render_template('assignment8.html', data5=output)

@app.route('/assignment8/question7', methods=['GET', 'POST'])
def question7():
    if request.method == 'POST':
        cur = mysql.connection.cursor()

        cur.execute('select people.id,people.name_of_person from people join soldiers where people.id=soldiers.s_id;')
        mysql.connection.commit()

        output = cur.fetchall()
        return render_template('assignment8.html', data7=output)

if __name__ == "__main__":
    app.run(debug=True)
