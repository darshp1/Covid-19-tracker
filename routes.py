from flask import render_template, request,redirect,flash,session
from covid import Covid
from project import app,mysql,bcrypt
from flask_login import login_user,current_user,logout_user,login_required
from flask_mysqldb import MySQLdb
import pandas as pd
from bs4 import BeautifulSoup
import requests

@app.route('/home_page', methods=['GET', 'POST'])
def home_page():
	covid=Covid()
	world_ac=covid.get_total_active_cases()
	world_cc=covid.get_total_confirmed_cases()
	world_rc=covid.get_total_recovered()
	world_td=covid.get_total_deaths()
	return render_template('home.html',wac=world_ac,wcc=world_cc,wrc=world_rc,wtd=world_td, title= 'Home Page')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        Email = details['email']
        password=details['paswrd']
        cp=details['cpaswrd']
        if(password!=cp):
        	return "password and confirm password must match"
       	else:
       		cur = mysql.connection.cursor()
       		p1=[firstName]
	        name1=cur.execute("Select name from flaskuser")
	        count1=cur.execute('Select * from flaskuser where name=%s',p1)
	        if name1>0:
	        	all_name=cur.fetchall()
	        p2=[Email]
	        email1=cur.execute("Select email from flaskuser")
	        count2=cur.execute('Select * from flaskuser where email=%s',p2)
	        if email1>0:
	        	all_email=cur.fetchall()
	        password1=cur.execute("Select pass from flaskuser")
	        if password1>0:
	        	all_password=cur.fetchall()
	        confirm_password1=cur.execute("Select cp from flaskuser")
	        if confirm_password1>0:
	        	all_confirm_password=cur.fetchall()
	        if(count1>0):
	        	flash('This name is already taken please choose another one or login if You have already registered once','fail')
	        	return render_template('p1.html')
	        if(count1==0):
	        	if(count2>0):
	        		flash("This Email is already taken please choose another one or login if You have already registered once",'fail')
	        		return render_template('p1.html')
	        	if(count2==0):
		       		hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
		       		cp=hash_password
			        cur.execute("INSERT INTO flaskuser(name, email , pass , cp) VALUES (%s, %s , %s , %s)", (firstName, Email,password,cp))
			        mysql.connection.commit()
			        cur.close()
			        return redirect('/home_page')
    return render_template('p1.html',title='Register')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM flaskuser WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
        if len(user) > 0:
        	pas=user["pass"]
        	if password==pas:
        		session['name'] = user['name']
        		session['email'] = user['email']
        		return redirect('/home_page')
        	else:
        		flash("Error password and email not match please enter correct password",'fail')
        		return render_template('login.html')
        else:
            return "Error user not found"
    else:
        return render_template('login.html')

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("p1.html")

@app.route('/world')
def world():
	covid=Covid()
	covid1 = Covid(source="worldometers")
	data=covid1.get_data()
	return render_template("world.html", data = data )
'''
	italy=covid.get_status_by_country_name("italy")
	data={
		key : italy[key]
		for key in italy.keys() and {'active','confirmed','deaths','recovered'}
	}
'''
@app.route('/india')
def india():
	url = 'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_India'# make a GET request to fetch the raw HTML content
	web_content = requests.get(url).content# parse the html content
	soup = BeautifulSoup(web_content, "html.parser")# remove any newlines and extra spaces from left and right
	extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
	city = [] 
	number=[]
	t1= soup.find('table', attrs={'style':'text-align:right; font-size:85%; width:100px; margin:0px 0px 0em 0em;'})
	tr=t1.find_all('tr')
	extract_contents = lambda num: [x.replace('\n', '') for x in num]
	extract_contents2 = lambda num: [x.replace('\n', '') for x in city]
	for row in tr:
	    try:
	    	name = row.find('th').get_text()
	    	city.append(name)
	    except:
	    	continue

	    try:
	    	num= row.find_all('td')
	    	for x in num:
	    		y=x.get_text()
	    		number.append(y)
	    except:
	    	continue
	        #now convert the data into a pandas dataframe for further processing
	number=extract_contents(number)
	city=extract_contents2(city)
	del city[:3]
	o=0
	cinema=[]
	for i1,j in enumerate(number):
	    p1=[]
	    for i in range(4):
	        p1.append(number[i+o])
	    cinema.append(p1)
	    o+=4
	    if o>=144:
	        break
	city=enumerate(city)
	return render_template("india.html",city=city,num=cinema)


@app.route('/States',methods=['GET','POST'])
def States():
	if request.method == "POST":
		sname=request.form.get("Gujarat",None)
		sname1=request.form.get("Maharashtra",None)
		sname2=request.form.get("Rajasthan",None)
		sname3=request.form.get("Punjab",None)
		sname4=request.form.get("Bihar",None)
		sname5=request.form.get("Kerala",None)
		sname6=request.form.get("Tamil_Nadu",None)

		if sname6:
			url = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Tamil_Nadu'# make a GET request to fetch the raw HTML content
			web_content = requests.get(url).content# parse the html content
			soup = BeautifulSoup(web_content, "html.parser")# remove any newlines and extra spaces from left and right
			extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
			city = [] 
			number=[]
			t1= soup.find('table', attrs={'style':'text-align:right; font-size:90%; margin:0px 0px 0em 0em;'})
			tr=t1.find_all('tr')

			extract_contents = lambda num: [x.replace('\n', '') for x in num]
			extract_contents2 = lambda num: [x.replace('\n', '') for x in city]
			for x in tr:
			    try:
			        num= x.find_all('td')
			        for x in num:
			            y=x.get_text()
			            number.append(y)
			    except:
			        continue

			number=extract_contents(number)
			del number[-1:]
			cinema=[]
			o=0

			print(number)
			print(len(number))
			for i1,j in enumerate(number):
			    p1=[]
			    for i in range(7):
			        p1.append(number[i+o])
			    cinema.append(p1)
			    o+=7
			    if o>=259:
			        break
						
			return render_template("States.html",num=cinema,sname6=sname6)

		if sname5:
			url = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Kerala'# make a GET request to fetch the raw HTML content
			web_content = requests.get(url).content# parse the html content
			soup = BeautifulSoup(web_content, "html.parser")# remove any newlines and extra spaces from left and right
			extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
			city = [] 
			number=[]
			t1= soup.find('table', attrs={'style':'text-align:right; font-size:85%; width:50px; float:left; clear:left; margin:0px 0px 0.5em 1em;'})
			tr=t1.find_all('tr')
			extract_contents = lambda num: [x.replace('\n', '') for x in num]
			extract_contents2 = lambda num: [x.replace('\n', '') for x in city]
			for row in tr:
			    try:
			    	name = row.find('a').get_text()
			    	city.append(name)

			    except:
			    	continue
			    try:
			    	num= row.find_all('td')
			    	for x in num:
			    		y=x.get_text()
			    		number.append(y)
			    except:
			    	continue
			        #now convert the data into a pandas dataframe for further processing
			number=extract_contents(number)
			city=extract_contents2(city)
			del city[:1]
			del city[-1:]
			cinema=[]
			o=0
			for i1,j in enumerate(number):
			    p1=[]
			    for i in range(4):
			        p1.append(number[i+o])
			    cinema.append(p1)
			    o+=4
			    if o>=56:
			        break
			city=enumerate(city)
			return render_template("States.html",city=city,num=cinema,sname5=sname5)

		if sname4:
			url = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Bihar'# make a GET request to fetch the raw HTML content
			web_content = requests.get(url).content# parse the html content
			soup = BeautifulSoup(web_content, "html.parser")# remove any newlines and extra spaces from left and right
			extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
			city = [] 
			number=[]
			t1= soup.find('table', attrs={'style':'text-align:right; font-size:90%; width:100px;'})
			tr=t1.find_all('tr')

			extract_contents = lambda num: [x.replace('\n', '') for x in num]
			extract_contents2 = lambda num: [x.replace('\n', '') for x in city]
			for row in tr:
			    try:
			    	name = row.find('a').get_text()
			    	city.append(name)

			    except:
			    	continue
			    try:
			    	num= row.find_all('td')
			    	for x in num:
			    		y=x.get_text()
			    		number.append(y)
			    except:
			    	continue
			        #now convert the data into a pandas dataframe for further processing
			number=extract_contents(number)
			city=extract_contents2(city)
			cinema=[]
			o=0
			for i1,j in enumerate(number):
			    p1=[]
			    for i in range(4):
			        p1.append(number[i+o])
			    cinema.append(p1)
			    o+=4
			    if o>=152:
			        break
			#print(city)
			#print(len(city))
			city=enumerate(city)
			#print(len(cinema))
			#print(cinema)
			return render_template("States.html",city=city,num=cinema,sname4=sname4)

		if sname3:
			url = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Punjab,_India'# make a GET request to fetch the raw HTML content
			web_content = requests.get(url).content# parse the html content
			soup = BeautifulSoup(web_content, "html.parser")# remove any newlines and extra spaces from left and right
			extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
			city = [] 
			number=[]
			t1= soup.find('table', attrs={'style':'text-align:right; font-size:90%; ar:right; margin:0px 0px 0.5em 1em;'})
			tr=t1.find_all('tr')
			#print(tr)
			extract_contents = lambda num: [x.replace('\n', '') for x in num]
			extract_contents2 = lambda num: [x.replace('\n', '') for x in city]
			for row in tr:
			    try:
			    	name = row.find('a').get_text()
			    	city.append(name)
			    except:
			    	continue
			    try:
			    	num= row.find_all('td')
			    	for x in num:
			    		y=x.get_text()
			    		number.append(y)
			    except:
			    	continue
			        #now convert the data into a pandas dataframe for further processing
			number=extract_contents(number)
			city=extract_contents2(city)
			del city[:1]
			del city[-1:]
			#city.remove('Total in Mumbai Metropolitan Region')
			#city.remove('District')
			#city.remove('Total (all districts)')
			'''
			for x in number:
			    if x=='':
			        number.remove('')
			'''
			cinema=[]
			o=0
			for i1,j in enumerate(number):
			    p1=[]
			    for i in range(3):
			        p1.append(number[i+o])
			    cinema.append(p1)
			    o+=3
			    if o>=66:
			        break
			#print(city)
			#print(len(city))
			city=enumerate(city)
			#print(cinema)
			#print(len(cinema))
			return render_template("States.html",city=city,num=cinema,sname3=sname3)


		elif sname2:
			city = [] 
			number=[]
			url = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Rajasthan'# make a GET request to fetch the raw HTML content
			web_content = requests.get(url).content# parse the html content
			soup = BeautifulSoup(web_content, "html.parser")# remove any newlines and extra spaces from left and right
			extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
			t1= soup.find('table', attrs={'style':'text-align:right; font-size:90%; width:100px; float:left; clear:left; margin:0px 0px 0.5em 1em;'})
			tr=t1.find_all('tr')
			extract_contents = lambda num: [x.replace('\n', '') for x in num]
			extract_contents2 = lambda num: [x.replace('\n', '') for x in city]
			for row in tr:
			    try:
			    	name = row.find('b').get_text()
			    	city.append(name)
			    except:
			    	continue
			    try:
			    	num= row.find_all('td')
			    	for x in num:
			    		y=x.get_text()
			    		number.append(y)
			    except:
			    	continue
			        #now convert the data into a pandas dataframe for further processing
			number=extract_contents(number)
			city=extract_contents2(city)
			for x in number:
			    if x=='':
			        number.remove('')

			cinema=[]
			
			o=0
			for i1,j in enumerate(number):
			    p1=[]
			    for i in range(4):
			        p1.append(number[i+o])
			    cinema.append(p1)
			    o+=4
			    if o>=132:
			        break
			del city[-6:]
			#print(city)
			#print(len(city))
			city=enumerate(city)
			#print(cinema)
			#print(len(cinema))
			return render_template("States.html",city=city,num=cinema,sname2=sname2)


		elif sname1:
				city = [] 
				number=[]
				url = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Maharashtra'# make a GET request to fetch the raw HTML content
				web_content = requests.get(url).content# parse the html content
				soup = BeautifulSoup(web_content, "html.parser")# remove any newlines and extra spaces from left and r
				t1= soup.find('table', attrs={'style':'text-align:right; font-size:90%; width:600px;'})
				tr=t1.find_all('tr')
				extract_contents = lambda num: [x.replace('\n', '') for x in num]
				extract_contents2 = lambda num: [x.replace('\n', '') for x in city]
				for row in tr:
				    try:
				    	name = row.find('th').get_text()
				    	city.append(name)
				    except:
				    	continue
				    try:
				    	num= row.find_all('td')
				    	for x in num:
				    		y=x.get_text()
				    		number.append(y)
				    except:
				    	continue
				        #now convert the data into a pandas dataframe for further processing
				number=extract_contents(number)
				city=extract_contents2(city)
				del city[:1]
				del city[-3:]
				city.remove('Total in Mumbai Metropolitan Region')
				#city.remove('District')
				#city.remove('Total (all districts)')
				#city.remove('Unknown')

				for x in number:
				    if x=='':
				        number.remove('')

				cinema=[]
				print(city)
				print(len(city))
				city=enumerate(city)
				o=0

				for i1,j in enumerate(number):
				    p1=[]
				    for i in range(3):
				        p1.append(number[i+o])
				    cinema.append(p1)
				    o+=3
				    if o>=105:
				        break
				print(cinema)
				print(len(cinema))
				return render_template("States.html",city=city,num=cinema,sname1=sname1)

		elif sname=="Gujarat":
			url = 'https://gujcovid19.gujarat.gov.in/'# make a GET request to fetch the raw HTML content
			web_content = requests.get(url).content# parse the html content
			soup = BeautifulSoup(web_content, "html.parser")# remove any newlines and extra spaces from left and right
			extract_contents = lambda row: [x.replace('\n', '') for x in city]
			extract_contents1 = lambda row: [x.replace('\r', '') for x in city]
			extract_contents = lambda num: [x.replace('\n', '') for x in num]
			extract_contents1 = lambda num: [x.replace('\r', '') for x in num]
			c=1
			city = [] 
			num=[]
			all_rows = soup.find_all('tr')
			for row in all_rows:
				try:
					name = row.find('td', attrs={'class':'text-left'}).get_text()
					city.append(name)
				except:
					continue
				try:
					stat = row.find_all('td', attrs={'class':'text-right'}) # notice that the data that we require is now a list of length 5
					if(stat):
						
						for numbers in stat:
							if(numbers):
								s = numbers.find('span').get_text()
								num.append(s)
				except:
					continue
				c+=1
			if(len(city)>0 and len(num)>0):
				city=extract_contents(city)
				city=extract_contents1(city)
				num=extract_contents1(extract_contents(num))
				cinema=[]
				o=0
				city=enumerate(city)
				for i1,j in enumerate(num):
					p1=[]
					for i in range(5):
						p1.append(num[i+o])
					cinema.append(p1)
					o+=5
					if o>=165:
						break

				return render_template("States.html",city=city,num=cinema,sname=sname)
			else:
				return "hello"

			'''
			if sname1:
			
				city = [] 
				number=[]
				url = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Maharashtra'# make a GET request to fetch the raw HTML content
				web_content = requests.get(url).content# parse the html content
				soup = BeautifulSoup(web_content, "html.parser")# remove any newlines and extra spaces from left and right
				extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
				t1= soup.find('table', attrs={'style':'text-align:right; font-size:90%; width:600px;'})
				tr=t1.find_all('tr')
				extract_contents = lambda num: [x.replace('\n', '') for x in num]
				extract_contents2 = lambda num: [x.replace('\n', '') for x in city]
				for row in tr:
				    try:
				    	name = row.find('th').get_text()
				    	city.append(name)
				    except:
				    	continue
				    try:
				    	num= row.find_all('td')
				    	for x in num:
				    		y=x.get_text()
				    		number.append(y)
				    except:
				    	continue
				        #now convert the data into a pandas dataframe for further processing
				number=extract_contents(number)
				city=extract_contents2(city)
				city.remove('Total in Mumbai Metropolitan Region')
				city.remove('District')
				city.remove('Total (all districts)')
				for x in number:
				    if x=='':
				        number.remove('')

				cinema=[]
				o=0
				for i1,j in enumerate(number):
				    p1=[]
				    for i in range(3):
				        p1.append(number[i+o])
				    cinema.append(p1)
				    o+=3
				    if o>=102:
				        break
''
				return render_template("States.html",sname1=sname1)
			else:
				return "hello"
'''
	else:
		return render_template("States.html")

@app.route('/users')
def users():
	cur=mysql.connection.cursor()
	result=cur.execute("Select * from flaskuser")
	if result>0:
		details=cur.fetchall()
		return render_template('users.html',details=details)

if __name__ == '__main__':
    app.run()


	