from datetime import datetime
from flask import render_template, url_for, flash, redirect,request,session
from flask_login import login_user,current_user, logout_user
from Restaurant import app,db
from Restaurant.model import User,reserve
from Restaurant.form import RegistrationForm, LoginForm

products = [
    {
        'id': 1,
        'name': 'Murthal Special',
        'image': '/static/images/menu/Murthalspepanner.webp',
        'price': 350
    },
    {
        'id': 2,
        'name': 'Shahi Paneer',
        'image': '/static/images/menu/Shahi-Paneer-1.jpg',
        'price': 350
    },
    {
        'id': 3,
        'name': 'Panner Butter',
        'image': '/static/images/menu/punnerbutter.webp',
        'price': 340
    },
    {
        'id': 4,
        'name': 'Kadhai Paneer',
        'image': '/static/images/menu/Kadai Paneer Recipe Restaurant style.jpg',
        'price': 360
    },
    {
        'id': 5,
        'name': 'Panner Do Pyaza',
        'image': '/static/images/menu/pannerpyaj.webp',
        'price': 330
    },
    {
        'id': 6,
        'name': 'Palak Paneer',
        'image': '/static/images/menu/palakpanner.webp',
        'price': 320
    },
    {
        'id': 7,
        'name': 'Chilli Paneer',
        'image': '/static/images/menu/chilipan.webp',
        'price': 340
    },
    {
        'id': 8,
        'name': 'Paneer Keema',
        'image': '/static/images/menu/pannerkeema.webp',
        'price': 320
    },
    {
        'id': 9,
        'name': 'Paneer Kali Mirch',
        'image': '/static/images/menu/pannerkalimirch.webp',
        'price': 320
    },
    {
        'id': 10,
        'name': 'Red Gravy Chaap',
        'image': '/static/images/menu/malaichaap red.webp',
        'price': 260
    },
    {
        'id': 11,
        'name': 'Changazi Chaap',
        'image': '/static/images/menu/changa=ezichaap.webp',
        'price': 280
    },
    {
        'id': 12,
        'name': 'Chaap Curry',
        'image': '/static/images/menu/chaapkari.webp',
        'price': 250
    },
    {
        'id': 13,
        'name': 'Kadhai Chaap',
        'image': '/static/images/menu/kadhaichhap.webp',
        'price': 260
    },
    {
        'id': 14,
        'name': 'Keema Chaap',
        'image': '/static/images/menu/kemmachaap.webp',
        'price': 290
    },
    {
        'id': 15,
        'name': 'Stuffed Chaap',
        'image': '/static/images/menu/stuffchaap.webp',
        'price': 320
    },
    {
        'id': 16,
        'name': 'Biryani',
        'image': '/static/images/menu/biryani.webp',
        'price': 200
    },
    {
        'id': 17,
        'name': 'Dal Makhani',
        'image': '/static/images/menu/dalmak.jpeg',
        'price': 230
    },
    {
        'id': 18,
        'name': 'Dum Aloo',
        'image': '/static/images/menu/dumallo.webp',
        'price': 220
    },
    {
        'id': 19,
        'name': 'Kadhi Chawal',
        'image': '/static/images/menu/kadhic.webp',
        'price': 150
    },
    {
        'id': 20,
        'name': 'Malai Kofta',
        'image': '/static/images/menu/malikoof.jpeg',
        'price': 320
    },
    {
        'id': 21,
        'name': 'Mix Veg',
        'image': '/static/images/menu/mixveg.webp',
        'price': 220
    },
    {
        'id': 22,
        'name': 'Mushroom Gravy',
        'image': '/static/images/menu/mushroom.webp',
        'price': 250
    },
    {
        'id': 23,
        'name': 'Stuff Naan',
        'image': '/static/images/menu/stuffnaan.webp',
        'price': 60
    },
    {
        'id': 24,
        'name': 'Special Murthal Naan',
        'image': '/static/images/menu/specialnnam.webp',
        'price': 70
    },
    {
        'id': 25,
        'name': 'Lacha Paratha',
        'image': '/static/images/menu/lacha.jpg',
        'price': 40
    }
]

@app.route("/")
@app.route("/Main Page")
def home():
    return render_template('index.html',title='Home')


@app.route("/Specials")
def special():
    return render_template('special.html',title='Special',us='Sign/Log In')

@app.route("/menu")
def menu():
    return render_template('menu.html',title='Menu',us='Sign/Log In',products=products )

@app.route("/cart", methods=['POST'])
def cart():
    try:
        if request.method == 'POST':
            product_id = int(request.form.get('product_id'))
            for i in products:
                if i['id'] == product_id:
                    selected_product = i

            product = {
                "product_img": selected_product['image'],
                "product_name": selected_product['name'],
                "price": selected_product['price'],
                "quantity": 1
            }

            if 'shopcart' in session:
                print(session['shopcart'])
                product_in_cart = False
                for item in session['shopcart']:
                    if item['product_name'] == product['product_name']:
                        # If the product is already in the cart, increment its quantity
                        print('new quantity')
                        item['quantity'] += 1
                        product_in_cart = True
                        break
                if not product_in_cart:
                    session['shopcart'].append(product)
            else:
                session['shopcart'] = [product]

            # Save the changes to the session
            session.modified = True

    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('menu'))



@app.route("/login", methods=['GET', 'POST'])
def registerlog():
    if current_user.is_authenticated:
         redirect (url_for('home'))

    regform = RegistrationForm()
    logform = LoginForm()
    if regform.validate_on_submit():
        user = User(username=regform.username.data, email=regform.email.data, password=regform.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {regform.username.data}!', 'success')
        login_user(user, remember=regform. remember .data)
        return redirect(url_for('home'))
    elif logform.validate_on_submit():
        user = User.query.filter_by(email=logform.email.data).first()
        if user and user.password==logform.password.data :
            flash('You have been logged in!', 'success')
            login_user(user, remember=logform.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Sign Up/Login', regform=regform,logform=logform)

@app. route ("/logout")
def logout():
  logout_user ()
  redirect (url_for('home'))

@app.route("/reserve",methods=['GET','POST'])
def make_reservation():
    names=request.form.get('fname')
    phone=request.form.get('phno')
    seats=request.form.get('nos')
    date=request.form.get('dandt')
    date_time_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M")

    reservation=reserve(name=names,phone=phone,seats=seats,dateandtime=date_time_obj)
    db.session.add(reservation)
    db.session.commit()
    users = reserve.query.all()
    for user in users:
        print(user.name, user.dateandtime)
    flash(f'Reservation booked for {names}', 'success')
    return redirect(url_for('home'))
    


