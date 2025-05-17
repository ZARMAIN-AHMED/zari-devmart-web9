import os
import streamlit as st
from auth import login, register
from database import products, user_carts, save_products
from models.product import Product
from models.payment import Payment
from models.cart import Cart
from utils import require_login



st.set_page_config(page_title="DevMart – Python Marketplace")
st.image("assets/dev.png", width=100)


if "user" not in st.session_state:
    st.session_state.user = None


if not st.session_state.user:
    st.title("🛍️ Welcome to DevMart!")
    st.subheader("Eco-friendly E-commerce Platform")

    email_capture = st.text_input("📩 Enter your email to get early offers")
    if st.button("Join Now"):
        if email_capture:
            st.success(f"Thanks for joining DevMart, {email_capture}!")
            st.balloons()

    st.markdown("### 🔐 Login or Register to Start Shopping")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user = login(email, password)
            if user:
                st.session_state.user = user
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials.")

    with tab2:
        name = st.text_input("Name", key="reg_name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_pass = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            user = register(name, reg_email, reg_pass)
            if user:
                st.success("Registration successful. You can log in now!")
            else:
                st.error("User already exists.")
    st.stop()

# Main App
require_login()


st.title(f"Welcome, {st.session_state.user.name}! 🛍️")

if st.button("Logout"):
    st.session_state.user = None
    if os.path.exists("session.json"):
        os.remove("session.json")
    st.rerun()

# Initialize cart
email = st.session_state.user.email
if email not in user_carts:
    user_carts[email] = Cart()

# Upload Product Section
st.divider()
st.header("📦 Upload a New Product")

with st.form("upload_form"):
    prod_name = st.text_input("Product Name")
    prod_desc = st.text_area("Description")
    prod_price = st.number_input("Price (USD)", min_value=0.0, step=0.01)
    submit = st.form_submit_button("Upload Product")

    if submit:
        if prod_name and prod_desc and prod_price > 0:
            new_product = Product(prod_name, prod_desc, prod_price)
            products.append(new_product)
            save_products(products)
            st.success(f"✅ Product '{prod_name}' uploaded successfully!")
        else:
            st.warning("⚠️ Please fill all fields correctly.")

st.header("🛒 Available Products")
for product in products:
    with st.container():
        st.subheader(product.name)
        st.caption(product.description)
        st.write(f"💵 ${product.price}")
        if st.button(f"Add to Cart - {product.name}"):
            user_carts[email].add_item(product)
            st.success(f"{product.name} added to cart!")


st.divider()
st.header("🧺 Your Cart")
cart = user_carts[email]

if cart.items:
    subtotal = cart.total()

    
    transaction_fee = round(subtotal * 0.50, 2)
    total_with_fee = round(subtotal + transaction_fee, 2)

    st.write(f"Subtotal: **${subtotal}**")
    st.write(f"Transaction Fee (50%): **${transaction_fee}**")
    st.write(f"🧾 Total (Including Fees): **${total_with_fee}**")

    if st.button("💳 Pay Now"):
        payment = Payment(st.session_state.user, total_with_fee)
        checkout_url = payment.process_payment()
        if checkout_url:
            st.success("Redirecting to payment...")
            st.markdown(f"[🟢 Click here to pay securely via Stripe]({checkout_url})", unsafe_allow_html=True)
        else:
            st.error("Payment setup failed. Try again.")
else:
    st.info("Your cart is empty.")

