from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import User, From, To
from django.contrib import messages
from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup
from pytz import timezone
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from math import cos, asin, sqrt
import requests
def index(request):
    return render(request,"one_app/introduction.html")


def login_registration(request):
    return render(request, "one_app/login_registration.html")


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/login_registration')
    else:
        check_user_email = User.objects.filter(email = request.POST['email'])

        if len(check_user_email)>0:
            messages.error(request, 'email already exist', extra_tags='email')
            return redirect('/login_registration')
        else :
            first_name = request.POST['first_name']
            email = request.POST['email']
            last_name = request.POST['last_name']
            password = bcrypt.hashpw(request.POST['password1'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=first_name, email=email, last_name=last_name, password=password)
            request.session['user_id'] = user.id
            return redirect(f"/driver_or_passenger")



def login(request):
    user = User.objects.filter(email=request.POST['login_email'])
    if user:
        if bcrypt.checkpw(request.POST['login_password'].encode(), user[0].password.encode()):
            request.session['user_id']=user[0].id
            return redirect(f"/driver_or_passenger")
    else:
        messages.error(request, 'email or password is wrong', extra_tags='login_error')
        return redirect('/login_registration')

def driver_or_passenger(request):
    user_name = User.objects.get(id=request.session['user_id'])
    print(user_name)
    return render(request, "one_app/driver_or_passenger.html")

def driver_add_departure(request):
    return render(request, "one_app/driver_add_departure.html")


def driver_add_departure_process(request):
    address = {
        'street': request.POST['street'],
        'city': request.POST['city'],
        'state': request.POST['state'],
        'zipcode': request.POST['zipcode'],
        'driver': request.session['user_id'],
        'time': request.POST['time'],
        'date' : request.POST['date']
    }
    driver=User.objects.get(id=request.session['user_id'])
    #result = test_address(address)
    result=True   # temporary remove when deploy
    if result == False:
        messages.error(request, 'Invalid address', extra_tags='invalid_Address')
        return redirect('/driver_add_departure')
    if result == True:
        new_departure = From.objects.create(street=address['street'], city=address['city'], state=address['state'], driver=driver, date=address['date'], time=address['time'])
        request.session['trip_id']=new_departure.id
        return redirect("/driver_add_arrival")


def driver_add_arrival(request):
    return render(request, "one_app/driver_add_arrival.html")


def driver_add_arrival_process(request):
    address = {
        'street': request.POST['street'],
        'city': request.POST['city'],
        'state': request.POST['state'],
        'zipcode': request.POST['zipcode'],
        'duration': request.POST['duration'],
        'price': request.POST['price']
    }
    #result = test_address(address)
    result=True
    if result == False:
        messages.error(request, 'Invalid address', extra_tags='invalid_Address')
        return redirect('/driver_add_arrival')
    if result == True:
        depart=From.objects.get(id=request.session['trip_id'])
        
        a=To.objects.create(from_where=depart,street=address['street'], city=address['city'],zipcode=address['zipcode'], state=address['state'],  price=address['price'],  estimate_time_arrival=address['duration'])
        return redirect(f'/driver_summary')


def driver_summary(request):
    context = {
    	'summary1' : From.objects.get(id=request.session['trip_id']),
        'summary2' : To.objects.get(from_where=request.session['trip_id'])
    }
    return render(request, "one_app/driver_summary.html", context)


def passenger(request):
    return render(request, "one_app/passenger.html")


def passenger_process(request):
    address = {
        'street': request.POST['street'],
        'city': request.POST['city'],
        'state': request.POST['state'],
        'zipcode': request.POST['zipcode'],
    }
    # result = test_address(address)
    # result=True
    # if result == False:
    #     messages.error(request, 'Invalid address', extra_tags='invalid_Address')
    #     return redirect('/passenger')
    # if result == True:        
    #     return HttpResponse('hahahah')
    results = From.objects.filter(date=request.POST['date'])
    print(results)
    locations=[]
    for i in range (0,len(results)):
        location = results[i].to.street+' '+results[i].to.city
        response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key=AIzaSyBHat7GUB_7DzbenFgIYvgxlyjvbnG19-o')
        resp_json_payload = response.json()
        result1=(resp_json_payload['results'][0]['geometry']['location'])
        locations.append({
                'lat':result1['lat'],
                'lng':result1['lng']
        })
    print(locations)
    input = request.POST['street']+' '+ request.POST['city']
    response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={input}&key=AIzaSyBHat7GUB_7DzbenFgIYvgxlyjvbnG19-o')
    resp_json_payload = response.json()
    result=(resp_json_payload['results'][0]['geometry']['location'])
    content={
        'lat':result['lat'],
        'lng':result['lng'],
        'locations':locations
    }
    print(content)
    return render(request, "one_app/passenger_temp.html", content)
    

def test_address(address):
    auth_id = "9484953c-80e6-c55d-c6fc-317df18233eb"
    auth_token = "GdjMKksY6pLKQFoLMiWx"
    credentials = StaticCredentials(auth_id, auth_token)
    client = ClientBuilder(credentials).build_us_street_api_client()
    lookup = Lookup()
    lookup.street = address['street']
    lookup.city = address['city']
    lookup.state = address['state']
    lookup.zipcode = address['zipcode']
    lookup.match = "Invalid"  # "invalid" is the most permissive match

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result

    if not result:
        print("No candidates. This means the address is not valid.")
        return False

    first_candidate = result[0]

    print("Address is valid. (There is at least one candidate)\n")
    print("ZIP Code: " + first_candidate.components.zipcode)
    print("County: " + first_candidate.metadata.county_name)
    print("Latitude: {}".format(first_candidate.metadata.latitude))
    print("Longitude: {}".format(first_candidate.metadata.longitude))
    return True