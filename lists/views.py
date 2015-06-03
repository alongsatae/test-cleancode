from django.shortcuts import redirect, render

from django.http import HttpResponse

from lists.models import Item
# Create your views here.

def home_page(request):
	#return HttpResponse('<html><title>To-Do lists</title></html>')

#	item = Item()
#	item.text = request.POST.get('item_text', '')
#	item.save()

#	return render(request, 'home.html', {'new_item_text': request.POST.get('item_text',''),
#		})

	if request.method == 'POST':
		new_item_text = request.POST['item_text']
		Item.objects.create(text=new_item_text)	#save() 호출이 필요없는 축약 명령
		return redirect('/lists/the-only-list-in-the-world/')
	#else:
	#	new_item_text = ''

	#items = Item.objects.all()
	#return render(request, 'home.html', {'new_item_text': new_item_text})
	return render(request, 'home.html')

def view_list(request):
	items = Item.objects.all()
	return render(request, 'list.html', {'items':items})