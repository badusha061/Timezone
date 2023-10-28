from django.shortcuts import render , redirect
from .forms import OfferForm
from .models import Offer
from django.shortcuts import  HttpResponseRedirect
from django.contrib import messages
# Create your views here.

def offer(request):
    form = OfferForm()
    offer = Offer.objects.all()
    context = {
        'form':form,
        'offer':offer
    }
    return render(request, 'adminside/offer.html',context)


def add_offer(request):
    try:
        if request.method == 'POST':
            form = OfferForm(request.POST)
            if form.is_valid():
                offername = form.cleaned_data['offer_name']
                discount = form.cleaned_data['discount_amount']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                if offername.strip() == '':
                    messages.error(request, 'Offer Name feilds is already existed')
                    return redirect('offer')

                if Offer.objects.filter(offer_name=offername).exists():
                    messages.error(request, 'Offer Name is already taken')
                    return redirect('offer')
                elif end_date <= start_date:
                    form.add_error('end_date', 'End date must be after the start date.')
                    messages.error(request,'End date must be after the start date.')
                    return render(request, 'adminside/offer.html',{'form':form})
                else:                   
                    form.save()
                    messages.success(request, 'Successfully Added')
                    print('saved')
                    return redirect('offer')
            else:
                print('form is not valid',form.errors)
                messages.error(request , 'Form is not valid')
                return redirect('offer')
                
        else:
            print('showings callings')
            form = OfferForm()
            return render(request, 'adminside/offer.html',{'form':form})
    except Exception as e:
        print(e)
        return render(request, 'adminside/offer.html')


def delete_offer(request,deleteoffer_id):
    try:
        dele = Offer.objects.get(id =deleteoffer_id)
        dele.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('offer')
    except Exception as e:
        print(e)
        return redirect('offer')
    
def edit_offer(request,editoffer_id):
    try:
        if request.method  == 'POST':
            offername = request.POST.get('offername')
            discount = request.POST.get('discount')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            
            if offername.strip() == '':
                messages.error(request, 'Offer Name feilds is already existed')
                return redirect('offer')

            if Offer.objects.filter(offer_name=offername).exists():
                messages.error(request, 'Offer Name is already taken')
                return redirect('offer')
            if discount.strip() == '':
                messages.error(request, 'the fields is empty')
                return redirect('offer')
            item = Offer.objects.get(id =editoffer_id )
            item.offer_name = offername
            item.discount_amount = discount
            item.start_date = start_date
            item.end_date = end_date
            item.save()
            messages.success(request,'Succesfully edited')
        return redirect('offer')
    except Exception as e:
        print(e)
        return redirect('offer')