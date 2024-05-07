from datetime import datetime
import secrets
from flask import render_template, url_for, flash, redirect,request,session,jsonify
from flask_login import login_user,current_user, logout_user,login_required
from Restaurant import app,db
from Restaurant.model import User,reserve,CustomerOrder
from Restaurant.form import RegistrationForm, LoginForm
import stripe

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
@app.route("/editmenu",methods=['POST'])
def editmenu():
    if request.method == 'POST':
        file = request.files['item-image']
        name=request.form.get('item-name')
        price=request.form.get('item-price')
        filen='/static/images/menu/'+ file.filename
        item={'id':len(products)+1,'name':name,'image':filen,'price':price}
        products.append(item)
        print(products[-2:])
        if file:
            
            # Save the file to a specific folder
            file.save(filen)
            return 'File uploaded successfully'
    

@app.route("/Specials")
def special():
    return render_template('special.html',title='Special',us='Sign/Log In')

@app.route("/menu")
def menu():
    return render_template('menu.html',title='Menu',us='Sign/Log In',products=products )
#Add to cart
@app.route("/cart", methods=['GET','POST'])
def cart():
    total=0
    if 'shopcart' in session:
        for i in session['shopcart']:
            total+=(i['price']*i['quantity'])

    return render_template('cart.html',title='Cart',total=total)

@app.route("/addtocart", methods = ['POST'])
def addtocart():
    try:
        # if request.method == 'POST':
            product_id = request.json['pid']
            for i in products:
                print(i['id'])
                if i['id'] == int(product_id):
                    selected_product = i
                    break
            
            product = {
                "product_img": selected_product['image'],
                "product_name": selected_product['name'],
                "price": selected_product['price'],
                "quantity": 1
            }

            if 'shopcart' in session:
                # print(session['shopcart'])
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
        return jsonify({'cart_count': len(session['shopcart'])})
    

@app.route('/get_cart_count', methods=['GET'])
def get_cart_count():
    # Return JSON response with current cart count
    if  'shopcart' in session:
      return jsonify({'cart_count': len(session.get('shopcart'))})
    else:
        return  jsonify({'cart_count':0})


@app.route('/update_session', methods=['POST'])
def update_session():
    data = request.json  #  data is sent as JSON
    itemname = list(data.keys())[0]  # Extract the item name from the JSON data
    quantity = data[itemname]  # Extract the quantity from the JSON data
    # Update session['shopcart'] with the new quantity
    for item in session['shopcart']:
        if item['product_name'] == itemname:
            if quantity==0:
                session['shopcart'].remove(item)
            else:
                item['quantity'] = quantity
            break
    session.modified = True   # Mark the session as modified
    if len(session['shopcart'])==0:
        return redirect(url_for('cart'))
    
    return jsonify({'status': 'success'})

#Login page
@app.route("/login", methods=['GET', 'POST'])
def registerlog():
    if current_user.is_authenticated:
        return redirect (url_for('home'))

    regform = RegistrationForm()
    logform = LoginForm()
    if regform.validate_on_submit():
        user = User(username=regform.username.data, email=regform.email.data, password=regform.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {regform.username.data}!', 'success')
        login_user(user)
        return redirect(url_for('home'))
    elif logform.validate_on_submit():
        user = User.query.filter_by(email=logform.email.data).first()
        if user and user.password==logform.password.data :
            if user.username==	"admin":
                login_user(user, remember=logform.remember.data)
                return redirect(url_for('admin'))
            flash('You have been logged in!', 'success')
            login_user(user, remember=logform.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Sign Up/Login', regform=regform,logform=logform)
@app.route("/admin")
def admin():
    return render_template('admin.html',title='Admin')
@app. route ("/logout")
def logout():
  logout_user()
  return redirect (url_for('home'))

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
    # users = reserve.query.all()
    # for user in users:
    #     print(user.name, user.dateandtime)
    flash(f'Reservation booked for {names}', 'success')
    return redirect(url_for('home'))
    

@app.route('/getorder')
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['shopcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('shopcart')
            flash('Your order has been sent successfully','success')
            return redirect(url_for('home'))  #HAVE TO CHANGE,invoice
        except Exception as e:
            print(e,"med")
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('cart'))
    else:
        flash('You need to login First','warning')
        return  redirect(url_for('registerlog'))
        
