from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from ComicShop.forms import UserRegistrationForm, UserProfileForm, AddToCartForm, CreditCardForm
from ComicShop.models import Comic, ShoppingCart, ComicInOrder

# Create your views here.


def index(request):
    genre = request.GET.get('genre')
    search_query = request.GET.get('search')
    comics = Comic.objects.order_by('price').all()
    user_profile = request.user

    if genre:
        comics = comics.filter(genre=genre)

    if search_query:
        comics = comics.filter(
            Q(name__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(publisher__icontains=search_query)
        )

    context = {'comics': comics, 'selected_genre': genre, 'search_query': search_query, 'user_profile': user_profile}

    return render(request, 'index.html', context=context)


def comic_detail(request, comic_id):
    comic = get_object_or_404(Comic, pk=comic_id)
    context = {'comic': comic}

    return render(request, 'comic_detail.html', context=context)


@login_required
def cart(request):
    shopping_cart = get_object_or_404(ShoppingCart, dedicated_user=request.user.userprofile)
    comic_in_orders = ComicInOrder.objects.filter(cart=shopping_cart)
    total_price = 0

    for comic_in_order in comic_in_orders:
        total_price += comic_in_order.comic.price * comic_in_order.quantity_added

    context = {
        'shopping_cart': shopping_cart,
        'comics': comic_in_orders,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    shopping_cart, created = ShoppingCart.objects.get_or_create(dedicated_user=request.user.userprofile)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            if quantity > comic.quantity_in_stock:
                messages.error(request, f"Quantity exceeds available stock for {comic.name}.")
                return redirect('comic_detail', comic_id=comic_id)

            comic_in_order, created = ComicInOrder.objects.get_or_create(comic=comic,
                                                                         cart=shopping_cart,
                                                                         defaults={'quantity_added': 0})
            if created:
                comic_in_order.quantity_added = quantity
                comic_in_order.save()
            else:
                comic_in_order.quantity_added += quantity
                comic_in_order.save()

            return redirect('cart')
    else:
        form = AddToCartForm()

    return redirect('cart')


@login_required
def remove_from_cart(request, comic_in_order_id):
    comic_in_order = get_object_or_404(ComicInOrder, id=comic_in_order_id)

    if request.method == 'POST':
        if comic_in_order.quantity_added > 1:
            comic_in_order.quantity_added -= 1
            comic_in_order.save()
        else:
            comic_in_order.delete()

    return redirect('cart')


@login_required
def remove_all_from_cart(request, comic_in_order_id):
    comic_in_order = get_object_or_404(ComicInOrder, id=comic_in_order_id)

    if request.method == 'POST':
        comic_in_order.delete()

    return redirect('cart')


@login_required
def order_summary(request):
    user_profile = request.user.userprofile
    shopping_cart = ShoppingCart.objects.get(dedicated_user=user_profile)
    comic_in_order_items = shopping_cart.comicinorder_set.all()

    context = {'comic_in_order_items': comic_in_order_items}

    return render(request, 'order_summary.html', context=context)


@login_required
def checkout(request):
    user_profile = request.user.userprofile
    shopping_cart = ShoppingCart.objects.get(dedicated_user=user_profile)

    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():

            for comic_in_order in shopping_cart.comicinorder_set.all():
                comic = comic_in_order.comic

                if comic.quantity_in_stock < comic_in_order.quantity_added:
                    messages.error(request, f"Quantity exceeds available stock for {comic.name}.")
                    return redirect('cart')

                comic.quantity_in_stock -= comic_in_order.quantity_added
                comic.save()
                comic_in_order.delete()

            messages.success(request, "Order placed successfully!")
            return redirect('order_confirmation')
    else:
        form = CreditCardForm()

    context = {'user_profile': user_profile, 'form': form}

    return render(request, 'checkout.html', context=context)


@login_required
def order_confirmation(request):
    return render(request, 'order_confirmation.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('index')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    context = {'user_form': user_form, 'profile_form': profile_form}

    return render(request, 'registration/registration.html', context=context)


@login_required
def edit_profile(request):
    user = request.user
    user_profile = user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {'form': form}

    return render(request, 'edit_profile.html', context=context)


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')
