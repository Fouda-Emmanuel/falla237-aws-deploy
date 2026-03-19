from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegisterForm, LoginForm, ItemForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import guest_only
from django.contrib import messages
from .models import Item
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def chunk_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def home(request):
    recent_lost_items_qs = Item.objects.filter(status='lost').order_by('-created_at')[:6]  # maybe 6 for 2 groups of 3
    recent_found_items_qs = Item.objects.filter(status='found').order_by('-created_at')[:6]

    recent_lost_items = list(chunk_list(list(recent_lost_items_qs), 3))  # group by 3
    recent_found_items = list(chunk_list(list(recent_found_items_qs), 3))

    context = {
        'recent_lost_items': recent_lost_items,
        'recent_found_items': recent_found_items,
    }
    return render(request, 'index.html', context)



@guest_only()
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Authenticate and log the user in immediately
            authenticated_user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if authenticated_user is not None:
                login(request, authenticated_user)
            name = user.full_name.title().strip() if user.full_name else user.username
            messages.success(request, f"🎉 Great to have you, {name}! Your Falla237 account is now ready. 🚀")
            return redirect('home')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'register.html', context)

@guest_only()
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Show full name if available, else username
                user.username
                name = user.full_name.title().strip() if user.full_name else user.username
                messages.success(request, f"Good to see you again, {name}!")
                return redirect('home') 
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully. See you at Falla237!")
    return redirect('home')

@login_required
def post_lost_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.status = 'lost'
            item.save()
            return redirect('object_detail', item_id=item.id)
    else:
        form = ItemForm()
    return render(request, 'post_lost.html', {'form': form})


@login_required
def post_found_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.status = 'found'
            item.save()
            return redirect('object_detail', item_id=item.id)
    else:
        form = ItemForm()
    return render(request, 'post_found.html', {'form': form})


def object_detail_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item_detail.html', {'item': item})


@login_required
def update_object_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if item.user != request.user:
        return render(request, 'unauthorized.html', status=403)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully!!!")
            return redirect('dashboard')
    else:
        form = ItemForm(instance=item)

    return render(request, 'edit_object.html', {'form': form, 'item': item})

@login_required
def delete_object_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.user != request.user:
        return render(request, 'unauthorized.html', status=403)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item deleted successfully.")
        return redirect('dashboard')



@login_required
def dashboard(request):
    items = Item.objects.filter(user=request.user).order_by('-created_at')

    # Add pagination
    paginator = Paginator(items, 5)  # Show 6 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'items': page_obj,  # Use page_obj for iteration
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'dashboard.html', context)


def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')


def lost_view(request):
    items = Item.objects.filter(status='lost').order_by('-created_at')

    # Filters
    location = request.GET.get('location')
    category = request.GET.get('category')
    date = request.GET.get('date')
    query = request.GET.get('q')

    if location:
        items = items.filter(location=location)
    if category:
        items = items.filter(category=category)
    if date:
        items = items.filter(date_lost_or_found=date)
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # Pagination
    paginator = Paginator(items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'items': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),

        'location_choices': Item.LOCATION_CHOICES,
        'category_choices': Item.CATEGORY_CHOICES,
    }
    return render(request, 'lost_objects.html', context)




def found_view(request):
    items = Item.objects.filter(status='found').order_by('-created_at')

    # Filters
    location = request.GET.get('location')
    category = request.GET.get('category')
    date = request.GET.get('date')
    query = request.GET.get('q')

    if location:
        items = items.filter(location=location)
    if category:
        items = items.filter(category=category)
    if date:
        items = items.filter(date_lost_or_found=date)
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # Pagination
    paginator = Paginator(items, 5)  # 6 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'items': page_obj,  # paginated items
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),

        # filters
        'location_choices': Item.LOCATION_CHOICES,
        'category_choices': Item.CATEGORY_CHOICES,
    }
    return render(request, 'found_objects.html', context)
