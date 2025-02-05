from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ContactForm,ReviewForm,SubscriberForm,CheckoutForm
from django.core.paginator import Paginator
import json
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from decimal import Decimal


def login_view(request):
    login_img = get_object_or_404(Master, name="login_img")
    
    if request.method == "POST":
        email = request.POST.get("email")  # Get email from the form
        password = request.POST.get("password")  # Get password from the form
        
        # Authenticate using email by checking the email and password manually
        try:
            user = User.objects.get(email=email)  # Get user by email
            if user.check_password(password):  # Check if the password is correct
                login(request, user)  # Django session-based login

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response = redirect("home")  # Redirect to home after login
                response.set_cookie("access_token", access_token, httponly=True, samesite="Lax")
                response.set_cookie("refresh_token", str(refresh), httponly=True, samesite="Lax")
                
                return response
            else:
                return render(request, "login.html", {"error": "Invalid credentials", "login_img": login_img})
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid credentials", "login_img": login_img})

    return render(request, "login.html", {"login_img": login_img})

def logout_view(request):
    logout(request)     # Clear session
    response = redirect("login")  # Redirect to login page
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

def signup_view(request):
    login_img = get_object_or_404(Master, name="login_img")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "signup.html")

        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return render(request, "signup.html")
        
        # Create new user
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save() # Log the user in after successful registration
            return redirect("login")  # Redirect to home page after successful sign-up
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "signup.html",{"login_img": login_img})
    
    return render(request, "signup.html",{"login_img": login_img})
@login_required
def home(request):
    home1_img = get_object_or_404(Master, name="home1_img")
    home2_img = get_object_or_404(Master, name="home2_img")
    home3_img = get_object_or_404(Master, name="home3_img")
    offer = Offer.objects.filter(is_active=True).order_by('-created_at').first()
    product=Product.objects.filter(featured=True)
    testimonials = Testimonial.objects.filter(is_active=True)[:5]
    print(product)
    print("this siiissssssssssssssssss",product)

    return render(request, 'ecommerce/index.html',{"home1_img":home1_img,"home2_img":home2_img,"home3_img":home3_img,'offer': offer,"products":product,'testimonials': testimonials})

def about(request):
    about_img = get_object_or_404(Master, name="about_img")
    return render(request,'ecommerce/about.html',{"about_img":about_img})
def shop(request):
    categories = Category.objects.all()  # Fetch all categories
    products = Product.objects.all()

    # If a category is selected from the filter, filter products by that category
    selected_category = request.GET.get('category')
    if selected_category:
        products = products.filter(category__id=selected_category)

    # Pagination logic
    paginator = Paginator(products, 8)  # Show 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare the rating for each product
    for product in page_obj:
        product.rating_range = range(product.rating)
        product.empty_rating_range = range(5 - product.rating)

    return render(request, 'ecommerce/product.html', {'page_obj': page_obj, 'categories': categories})


def contact_view(request):
    location = Master.objects.filter(category="City").first()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # Redirect to avoid resubmission
    else:
        form = ContactForm()

    return render(request, 'ecommerce/contact.html', {'form': form,'location': location})

def pp(request):
    return render(request,"ecommerce/privacy.html")
def terms(request):
    return render(request,"ecommerce/terms.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Subscriber
from .forms import SubscriberForm

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if the email already exists
            if Subscriber.objects.filter(email=email).exists():
                messages.error(request, "This email is already subscribed.")
            else:
                form.save()  # Save the new subscriber
                messages.success(request, "Thank you for subscribing! Check your inbox for the 30% discount.")
        else:
            messages.error(request, "Please enter a valid email address.")
    
    # Redirect back to the same page after handling the POST request
    return redirect(request.META.get('HTTP_REFERER', 'home'))



def singleproduct(request, product_id):
    # Fetch product from the database using product_id
    product = Product.objects.get(id=product_id)
    
    product.rating_range = range(product.rating)
    product.empty_rating_range = range(5 - product.rating)
    
    return render(request, 'ecommerce/single_product.html', {'product': product})

def shopping_cart(request):
    products = Product.objects.all()
    
    
    # Convert product data to JSON-serializable format
    product_data = {
        str(p.id): {
            "name": p.name,
            "price": float(p.price),  # ✅ Convert Decimal to float
            "image": p.image.url
        } 
        for p in products
    }

    return render(request, "ecommerce/shoppingcart.html", {"product_data": json.dumps(product_data)})
def get_cart_products(request):

    return render(request,"ecommerce\cart2.html")


# views.py

@csrf_exempt
def cart_view(request):
    if request.method == "POST":
        cart_data = json.loads(request.body)
        product_ids = [item['id'] for item in cart_data['cart']]

        # Fetch products from the database
        products = Product.objects.filter(id__in=product_ids)

        cart_products = []
        for product in products:
            # Use next() with a default value of None to avoid StopIteration error
            cart_item = next((item for item in cart_data['cart'] if item['id'] == str(product.id)), None)

            if cart_item is not None:
                cart_products.append({
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price),
                    'count': cart_item['count'],
                    'image': product.image.url if product.image else None,
                })
        print(cart_products)        

        return JsonResponse({'cart': cart_products})
    
 
def checkout1(request):
    if request.method == 'POST':
        # Step 1: Handle customer information
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Get cleaned data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']

            # Optionally, you can store this data in session to use in the following steps
            request.session['customer_info'] = {
                'name': name,
                'email': email,
                'address': address,
                'phone': phone
            }

            # Redirect to the next step (order summary or payment)
            return redirect('checkout')
        else:
            # If form is invalid, re-render with errors
            return render(request, 'ecommerce/checkout.html', {'form': form})

    # GET request: Show the checkout form
    form = CheckoutForm()
    return render(request, 'ecommerce/checkout.html', {'form': form})  


def checkout_step_2(request):
    # Step 2: Get customer info from the session
    customer_info = request.session.get('customer_info')

    if customer_info:
        name = customer_info.get('name')
        email = customer_info.get('email')
        address = customer_info.get('address')
        phone = customer_info.get('phone')
        print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",name)
        # Handle the order summary or other processing
        return render(request, 'ecommerce/checkout.html')
    else:
        # If no customer info in session, redirect to Step 1
        return redirect('checkout')
def checkout(request):
    # Assuming you have a cart stored in the session or database
    cart = json.loads(request.session.get('cart', '{}'))  # Retrieve the cart from session (or use localStorage data)

    cart_items = []
    total_price = 0

    for product_name, product_data in cart.items():
        product = Product.objects.get(name=product_name)  # Get the product details from the database
        total_price += product.price * product_data['quantity']
        cart_items.append({
            'name': product.name,
            'price': product.price,
            'quantity': product_data['quantity'],
            'total': product.price * product_data['quantity'],
            'image': product.image.url  # assuming you have a product image field
        })

    return render(request, 'ecommerce\checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

from django.contrib import messages

def confirm_order(request):
    if request.method == "POST":
        # Process the order
        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_success')  # Redirect to a success page or back to the home page
    

from django.http import JsonResponse
from .models import Product  # Assuming you have a Product model

def api_cart(request):
    if request.method == 'POST':
        cart_data = request.body.decode('utf-8')  # Get cart data from frontend
        cart = json.loads(cart_data)  # Parse JSON cart data

        cart_details = []
        for item in cart:
            product = Product.objects.get(id=item['id'])
            cart_details.append({
                'name': product.name,
                'price': product.price,
                'count': item['count'],
                'image': product.image.url  # Assuming your products have images
            })
        
        total_price = sum(item['price'] * item['count'] for item in cart_details)
        
        return JsonResponse({
            'cart': cart_details,
            'total_price': total_price
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)


