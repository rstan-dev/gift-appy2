from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required

from .models import Item
from .forms import WishForm
# Create your views here.
@login_required
def profile(request):
    """Renders the profile page"""
    context = {}
    return render(request, 'profiles/profile.html', context)


@login_required
def wishlist(request):
    """Renders the profile page"""
    user = request.user
    wishlist = Item.objects.filter(user=user)

    if request.method == 'POST':
        wish_form = WishForm(request.POST, request.FILES)
        if wish_form.is_valid():
            form = wish_form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect(reverse('wishlist'))
        else:
            messages.error(request, 'Error adding the product. \
                Verify that all fields are filled in accurately.')
    else:
        wish_form = WishForm()

    template_name = 'profiles/wishlist.html'
    context = {
        'wishlist': wishlist,
        'wish_form': wish_form,
    }
    return render(request, template_name, context)


def edit_wish(request, item_id):
    """ Render the Edit_wish template"""

    wish = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        wish_form = WishForm(request.POST, request.FILES, instance=wish)
        if wish_form.is_valid():
            wish_form.save()
            return redirect(reverse('wishlist'))
    else:
        wish_form = WishForm(instance=wish)

    template_name = 'profiles/edit_wish.html'
    context = {
        'wish_form': wish_form,
        'wish': wish,
    }
    return render(request, template_name, context)


@login_required
def delete_wish(request, item_id):
    """This function deletes a selected wish"""
    wish = get_object_or_404(Item, pk=item_id)
    wish.delete()
    return redirect('wishlist')
