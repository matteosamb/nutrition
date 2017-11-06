from django.shortcuts import render
from.forms import MacroSearch, RestaurantSearch
from nutritionix import Nutritionix
import json
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse

import html

# Create your views here.


#Search by restaurant
def restaurant(request):
    if request.method == 'POST':
        form = RestaurantSearch(data=request.POST)
        if form.is_valid():
            #Capture user input, assign it to variable 'name'
            name = form.cleaned_data['name']

            #Nutritionix API request
            nix = Nutritionix(app_id="a70d76f6", api_key="e0d08a959dacfd68dd69b5473f2fc41c")

            cal1 = nix.search(offset="0", limit="50").nxql(
                queries={
                    "brand_name":name,
                },

                fields=["item_name", "brand_name", "nf_calories", "nf_total_fat", "nf_protein", "nf_total_carbohydrate",
                        "nf_sodium"],

            ).json()
            response1 = json.dumps(cal1)
            a = json.loads(response1)
            b = (a.get("hits"))
            r = []

            for c in b:
                kitten = (c.get("fields").get("brand_name"))
                if kitten not in r:
                    r.append(kitten)
            context = {'form':form,'name':name,'r':r}
            return render(request, 'macro/restaurant.html', context)
    else:
        form = RestaurantSearch()
        context = {'form':form}
        return render(request, 'macro/restaurant.html', context)








def search(request):
    if request.method == 'POST':
        form = MacroSearch(data=request.POST)
        if form.is_valid():
            cal1 = form.cleaned_data['calmin']
            cal2 = form.cleaned_data['calmax']
            fat1 = form.cleaned_data['fatmin']
            fat2 = form.cleaned_data['fatmax']
            carb1 = form.cleaned_data['carbsmin']
            carb2 = form.cleaned_data['carbsmax']
            pro1 = form.cleaned_data['promin']
            pro2 = form.cleaned_data['promax']
            sod1 = form.cleaned_data['sodmin']
            sod2 = form.cleaned_data['sodmax']

            nix = Nutritionix(app_id="a70d76f6", api_key="e0d08a959dacfd68dd69b5473f2fc41c")

            cal = nix.search(offset="0", limit="50").nxql(
                filters={
                    "nf_calories": {
                        "from": cal1,
                        "to": cal2
                    },
                    "nf_total_fat": {
                        "from": fat1,
                        "to": fat2
                    },
                    "nf_total_carbohydrate": {
                        "from": carb1,
                        "to": carb2
                    },
                    "nf_protein": {
                        "from": pro1,
                        "to": pro2
                    },
                    "nf_sodium": {
                        "from": sod1,
                        "to": sod2
                    },
                    "item_type": 1,

                },

                fields=["item_name", "brand_name", "nf_calories", "nf_total_fat", "nf_protein", "nf_total_carbohydrate",
                        "nf_sodium"],

            ).json()

            response = json.dumps(cal)
            a = json.loads(response)
            b = (a.get("hits"))
            calories = []
            fat = []
            az = ['monkey','money','ham']
            protein = []
            carbs = []
            sodium = []
            itemname=[]
            restaurant=[]
            for c in b:
                kitten = (c.get("fields").get("brand_name"))
                restaurant.append(kitten)
                meal = (c.get("fields").get("item_name"))
                restaurant.append(meal)
                h = (c.get("fields").get("nf_calories"))
                restaurant.append(h)
                j = (c.get("fields").get("nf_total_fat"))
                restaurant.append(j)
                l = (c.get("fields").get("nf_protein"))
                restaurant.append(l)
                k = (c.get("fields").get("nf_total_carbohydrate"))
                restaurant.append(k)
                s = (c.get("fields").get("nf_sodium"))
                sodium.append(s)

            all = restaurant + itemname






            context = {'form':form,'b':b,'restuarant':restaurant,'protein':protein,'itemname':itemname,'calories':calories,'fat':fat,'protein':protein,'az':az}
    else:
        form = MacroSearch()
        context = {'form':form}
    return render(request,'macro/index.html',context)




def results(request):
    if request.method == 'GET':
        sku = request.GET.get('sku')

        nix = Nutritionix(app_id="a70d76f6", api_key="e0d08a959dacfd68dd69b5473f2fc41c")

        cal1 = nix.search(offset="0", limit="50").nxql(
            queries={
                "brand_name": sku,
            },

            fields=["item_name", "brand_name", "nf_calories", "nf_total_fat", "nf_protein", "nf_total_carbohydrate",
                    "nf_sodium"],

        ).json()
        response1 = json.dumps(cal1)
        a = json.loads(response1)
        b = (a.get("hits"))
        r = []
        blue = []
        aye = []



        for c in b:
            kitten = (c.get("fields").get("brand_name"))
            kitten1 = (c.get("fields").get("item_name"))
            kitten2 = (c.get("fields").get("nf_calories"))

            if kitten == sku:
                r.append(kitten)
                blue.append(kitten1)
                aye.append(kitten2)
        h = len(blue)


        context = {'sku':sku,'r':r,'blue':blue,'aye':aye,'h':h}
        return render(request, 'macro/results.html',context)

    else:
        return render(request, 'macro/results.html')