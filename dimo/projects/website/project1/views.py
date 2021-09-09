from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView, View
from project1.models import *
from django.contrib import messages
from django.utils import timezone
   



# Create your views here.
def base(response):
    return render(response, 'project1/base.html')
def home(response):
    
    slideimage = ImageSlider.objects.all()
    ceo = CeoImage.objects.all()
    background = BackgroundImage.objects.all()
    context= {"slideimage":slideimage, "ceo":ceo, "background":background}
    return render(response, 'project1/home.html', context)
def about(response):
    
    ourimage = OurImages.objects.all()
    headerimage = AboutHeaderImage.objects.all()
    paragraphimage = AboutImageOfParagraph.objects.all()
    context= {"ourimage":ourimage, "headerimage":headerimage, "paragraphimage":paragraphimage}
    return render(response, 'project1/about.html', context)



def product_list(response,category_slug=None):
   
    
    category = None
  

    categories = Category.objects.all()
    item = Item.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        item= item.filter(category=category)



    context = {"categories":categories, "category":category, "item":item}

    return render(response, 'project1/product_list.html', context)


#class ProductDetail(DetailView):
   # model = Item
   # template_name = 'project1/product.html'

def product_detail(response, id, slug):
   

    product_detail= get_object_or_404(Item,id=id, slug=slug)
   
    
    #viewdetail = Story.objects.get(id=pk)
  
    context= {"product_detail":product_detail}
    
    return render(response, 'project1/product_detail.html', context)



def add_to_cart(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_id=item.id, item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item}'s quantity was updated")
            return redirect('order_summary')
        else:
            order.items.add(order_item)
            messages.success(request, f"{item} was added to your Order")
            return redirect('order_summary')

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered=False, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, f"{item} was added to your Order")
        return redirect('order_summary')
    


def remove_from_cart(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_id=item.id, item__slug=item.slug).exists():
            order.items.remove(order_item)
            order.save()
            messages.success(request, f"{item.title} was removed from your Order")
                
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.title} was not in your Order")
            return redirect('order_summary')
    else:
        messages.info(request, "You don't have an active order!")
        return redirect('order_summary')


def remove_single_from_cart(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id, item__slug=item.slug).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order.save()
            messages.success(request, f"{item}'s quantity was updated")
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.title} was not in your Order")
            return redirect('order_summary')
    else:
        messages.info(request, "You don't have an active Order!")
        return redirect('order_summary')

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order':order
        }
        return render(self.request, 'project1/order_summary.html',context)

       