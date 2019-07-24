from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import Users, From, To
from django.contrib import messages
from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup
from datetime import datetime


def index(request):
    return render(request,"one_app/introduction.html")


def login_registration(request):
    return render(request, "one_app/login_registration.html")


def register(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/login_registration')
    else:
        check_user_email = Users.objects.filter(email = request.POST['email'])

        if len(check_user_email)>0:
            messages.error(request, 'email already exist', extra_tags='email')
            return redirect('/login_registration')
        else :
            first_name = request.POST['first_name']
            email = request.POST['email']
            last_name = request.POST['last_name']
            password = bcrypt.hashpw(request.POST['password1'].encode(), bcrypt.gensalt())
            user = Users.objects.create(first_name=first_name, email=email, last_name=last_name, password=password)
            request.session['user_id'] = user.id
            return redirect(f"/driver_or_passenger")



def login(request):
    user = Users.objects.filter(email=request.POST['login_email'])
    if user:
        if bcrypt.checkpw(request.POST['login_password'].encode(), user[0].password.encode()):
            request.session['user_id']=user[0].id
            return redirect(f"/driver_or_passenger")
    else:
        messages.error(request, 'email or password is wrong', extra_tags='login_error')
        return redirect('/login_registration')

def driver_or_passenger(request):
    user_name = Users.objects.get(id=request.session['user_id'])
    print(user_name)
    return render(request, "one_app/driver_or_passenger.html")

def driver_add_departure(request):
    return render(request, "one_app/driver_add_departure.html")


def driver_add_departure_process(request):
    address ={
        'street':request.POST['street'],
        'city': request.POST['city'],
        'state': request.POST['state'],
        'zipcode': request.POST['zipcode'],
        'time' : request.POST['time']     }

    # result = test_address(address)
    #
    # if result == False:
    #     messages.error(request, 'Invalid address', extra_tags='invalid_Address')
    #     return redirect('/driver_add_departure')
    # if result == True:
    #     new_departure = Users.objects.create(street=address['street'], city=email, state=last_name, time=time)
    result=address['time']
    result1=datetime.result.strftime('%Y-%m-%dT%H:%M:%S')

    myDate = datetime.now()

    return HttpResponse(result1)
    # return redirect(request, "one_app/driver_add_arrival.html")



def driver_add_arrival(request):

    return render(request, "one_app/driver_add_arrival.html")


def passenger(request):
    return render(request, "one_app/passenger.html")


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