from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem, UserActivity
from django.utils import timezone
from django.http import JsonResponse
import uuid
from django.shortcuts import render
from .models import UserActivity, Product
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

def stats_view(request):
    today = timezone.now().date()
    one_week_ago = today - timedelta(days=7)
    
    # Kullanıcı aktivitelerini gruplama
    user_activities = UserActivity.objects.filter(timestamp__date__gte=one_week_ago).values('session_id', 'action', 'product__name', 'timestamp__date').annotate(count=Count('id')).order_by('session_id', 'timestamp__date')

    # Ürün istatistiklerini toplama
    product_stats = {}
    for product in Product.objects.all():
        views = UserActivity.objects.filter(product=product, action='viewed', timestamp__date__gte=one_week_ago).count()
        added_to_cart = UserActivity.objects.filter(product=product, action='added_to_cart', timestamp__date__gte=one_week_ago).count()
        purchased = UserActivity.objects.filter(product=product, action='purchased', timestamp__date__gte=one_week_ago).count()
        product_stats[product.name] = {
            'views': views,
            'added_to_cart': added_to_cart,
            'purchased': purchased
        }

    return render(request, 'funnel/stats.html', {
        'user_activities': user_activities,
        'product_stats': product_stats,
        'one_week_ago': one_week_ago,
        'today': today,
    })



def get_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def track_user_activity(request, product=None, action='', page=''):
    session_id = get_session_id(request)
    UserActivity.objects.create(
        session_id=session_id,
        product=product,
        action=action,
        timestamp=timezone.now(),
        page=page
    )


def home(request):
    products = Product.objects.all()
    return render(request, 'funnel/home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    track_user_activity(request, product=product, action='viewed')
    return render(request, 'funnel/product_detail.html', {'product': product})

def cart_view(request):
    session_id = get_session_id(request)
    cart, created = Cart.objects.get_or_create(session_id=session_id)
    return render(request, 'funnel/cart.html', {'cart': cart})

def add_to_cart(request, product_id):
    session_id = get_session_id(request)
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(session_id=session_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    track_user_activity(request, product=product, action='added_to_cart')
    return redirect('cart_view')

def purchase(request):
    session_id = get_session_id(request)
    cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    if request.method == 'POST':
        # Ödeme işlemlerini burada gerçekleştirin
        
        # Her bir ürün için purchased aksiyonunu izleyin
        for item in cart.items.all():
            track_user_activity(request, product=item.product, action='purchased')
        
        # Sepeti temizleyin
        cart.items.all().delete()
        
        return redirect('lead_capture')
    
    return render(request, 'funnel/purchase.html', {'cart': cart})

def lead_capture(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        # Lead capture işlemlerini burada gerçekleştirin
        return redirect('home')
    return render(request, 'funnel/lead_capture.html')
