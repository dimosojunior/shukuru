from django.db import models
from django.shortcuts import reverse

from django.contrib.auth.models import User


#CATEGORY_CHOICES = (
   # ('S', 'Shirt'),
   # ('SW', 'SportWear'),
  #  ('OW', 'OutWear')
#)
#LABEL_CHOICES = (
  #  ('S', 'secondary'),
   # ('P', 'primary'),
   # ('D', 'danger')
#)

class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    
    slug=models.SlugField(unique=True)
    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'

    def _str_(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_by_category', args=[self.slug])

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()
    status = models.CharField(max_length=200)
    #category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    #label = models.CharField(choices=LABEL_CHOICES, max_length=2)
    description = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='productImages')
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug': self.slug, 'id': self.id})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug': self.slug, 'id': self.id})

    def get_remove_single_from_cart_url(self):
        return reverse('remove_single_from_cart', kwargs={'slug': self.slug, 'id': self.id})

    


class OrderItem(models.Model):
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_final_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()

   


class Order(models.Model):
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
   
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        
        return total
    

class ImageSlider(models.Model):
    
    image=models.ImageField(upload_to="img/%y")
    caption=models.CharField(max_length=200)
    title=models.CharField(max_length=200)
    content=models.TextField(max_length=1000)
    

    def _str_(self):
        return self.title


class CeoImage(models.Model):
   
    image=models.ImageField(upload_to="img/%y")
    caption=models.TextField(max_length=200)
    def _str_(self):
        return self.caption
class BackgroundImage(models.Model):
   
    image=models.ImageField(upload_to="img/%y")



#ABOUT.HTML MODES
  
    
class OurImages(models.Model):
    image=models.ImageField(upload_to="img/%y")
    caption=models.CharField(max_length=100)
    def _str_(self):
        return self.caption
class AboutHeaderImage(models.Model):
    image=models.ImageField(upload_to="img/%y")
    content=models.TextField(max_length=1000)
    def _str_(self):
        return self.content
    

class AboutImageOfParagraph(models.Model):
    image=models.ImageField(upload_to="img/%y")
    content=models.TextField(max_length=1000)
    title=models.CharField(max_length=1000)
    def _str_(self):
        return self.title
  

class Customer(models .Model):
    user = models.OneToOneField(User, null=False,blank=False,on_delete=models.CASCADE)

    phone_field = models.CharField(max_length=200)

    def _str_(self):
        return self.user.username 

