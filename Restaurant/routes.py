from datetime import datetime
import secrets
from flask import render_template, url_for, flash, redirect,request,session,jsonify
from flask_login import login_user,current_user, logout_user,login_required
from Restaurant import app,db
from Restaurant.model import User,reserve,CustomerOrder,products
from Restaurant.form import RegistrationForm, LoginForm
import os
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
         # Define the directory path where the file should be saved
        upload_dir = os.path.join(app.root_path, 'static/images/menu')

        # Ensure the directory exists
        os.makedirs(upload_dir, exist_ok=True)

        # Construct the full file path
        file_path = os.path.join(upload_dir, file.filename)
         # Save the file
        file.save(file_path)
        filen= 'static/images/menu'+file.filename
        prod_count = products.query.count()+1
        prod=products(id=prod_count,name=name,price=price,image_file=filen)
        db.session.add(prod)
        db.session.commit()
    return redirect(url_for('menu'))
    

@app.route("/Specials")
def special():
    return render_template('special.html',title='Special',us='Sign/Log In')

@app.route("/menu")
def menu():
    prod=products.query.all()
    return render_template('menu.html',title='Menu',us='Sign/Log In',products=prod )
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
            singleproduct = products.query.all()
            for i in singleproduct:
                if i.id == int(product_id):
                    selected_product = i
                    break
            
            product = {
                "product_img": selected_product.image_file,
                "product_name": selected_product.name,
                "price": selected_product.price,
                "quantity": 1
            }

            if 'shopcart' in session:
                # print(session['shopcart'])
                product_in_cart = False
                for item in session['shopcart']:
                    if item['product_name'] == product['product_name']:
                        # If the product is already in the cart, increment its quantity
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
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('cart'))
    else:
        flash('You need to login First','warning')
        return  redirect(url_for('registerlog'))
        
#  last_two_users = db.session.query(User).order_by(User.id.desc()).limit(2).all()

#     # Delete the last two records
#     for user in last_two_users:
#         db.session.delete(user)

#     # Commit the transaction to apply the changes
#     db.session.commit()
    