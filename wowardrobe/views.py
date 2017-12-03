from django.db.models import Count
from django.http import HttpResponse, Http404
from mimetypes import guess_type

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from wowardrobe.models import *
from django.core.exceptions import ObjectDoesNotExist
import urllib3
from urllib.parse import urlparse, urlencode
import json
import base64
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.contrib import messages
from django.core import serializers

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from wowardrobe.forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
import datetime
from django.db.models import Q
from random import randint
from django.shortcuts import render_to_response
from django.template import RequestContext
import operator

CONSTANT_COLORS = ['Beige', 'Black', 'Blue', 'Cream', 'Green', 'Pink', 'Red', 'Yellow', 'Brown', 'Purple', 'Multi']
CONSTANT_CATEGORY = ['Shirt', 'Blouse', 'Sweater', 'Cardigan', 'Jacket', 'Coat', 'Suit', 'Dress',
                     'Shorts', 'Skirt', 'Jeans', 'Pants', 'Sneakers', 'Boots', 'Slipper', 'Sandal', 'Heels','Flats']
CONSTANT_EVENT = ['Party', 'Work', 'School', 'Everyday', 'Interview', 'Travel', 'Work Out']
CONSTANT_BRAND = ['Asos','Adidas','Banana Republic','Gap','Nike','H&M','Levis', 'Madewell','Free People','Old Navy','Ralph Lauren','Under Armor']
CONSTANT_SEASON = ['Spring', 'Summer', 'Fall', 'Winter']
CONSTANT_TLEVEL = [1, 2, 3, 4, 5, 6]
CONSTANT_WEATHER = ['Sunny', 'Cloudy', 'Overcast', 'Rainy', 'Windy', 'Snowy']
CONSTANT_STYLE = ['Bohemian', 'Vintage', 'Cute', 'Sexy', 'Casual', 'Elegant', 'Tomboy', 'Rocker', 'Chic', 'Sporty',
                  'Professional', 'Preppy']
DICT = {'Jacket': [['Everyday', 'Travel'], ['Fall', 'Winter'], CONSTANT_WEATHER, [5], ['Casual']],
        'Sweater': [['Everyday'], ['Winter'], CONSTANT_WEATHER, [5], ['Casual']],
        'Shirt': [['Everyday'], ['Spring', 'Summer'], ['Sunny', 'Cloudy', 'Overcast'], [2], ['Casual']],
        'Shorts': [['Everyday'], ['Summer'], ['Sunny', 'Cloudy', 'Overcast', 'Rainy'], [2], ['Tomboy']],
        'Skirt': [['Everyday'], ['Summer'], ['Sunny', 'Cloudy', 'Overcast', 'Rainy'], [2], ['Casual']],
        'Jeans': [['Everyday'], CONSTANT_SEASON, CONSTANT_WEATHER, [3], ['Casual']],
        'Cardigan': [['Work'], ['Winter'], CONSTANT_WEATHER, [5], ['Professional']],
        'Suit': [['Work', 'Interview'], ['Spring', 'Summer', 'Fall'], ['Sunny', 'Cloudy', 'Overcast'], [3],
                 ['Professional']],
        'Dress': [['Work', 'Everyday', 'Party'], ['Spring', 'Summer', 'Fall'], ['Sunny', 'Cloudy', 'Overcast'], [3],
                  ['Elegant']],
        'Blouse': [['Work', 'Interview'], ['Spring', 'Summer', 'Fall'], ['Sunny', 'Cloudy', 'Overcast'], [3],
                   ['Professional', 'Elegant']],
        'Sneakers': [['Everyday', 'Travel'], ['Spring', 'Summer', 'Fall'], ['Sunny', 'Cloudy', 'Overcast', 'Rainy'],
                     [2], ['Sporty', 'Casual']],
        'Boots': [['Work'], ['Fall', 'Winter'], ['Sunny', 'Cloudy', 'Overcast', 'Rainy'], [5], ['Casual']],
        'Sandal': [['Work out'], ['Summer'], ['Sunday', 'Cloudy', 'Overcast'], [1], ['Casual']]}
CONSTANT_OUTWEAR = ['Coat', 'Jacket', 'Blazer']
CONSTANT_TOPS = ['Shirt', 'Blouse', 'Sweater', 'Cardigan', 'Suit', 'T-Shirt']
CONSTANT_BOTTOMS = ['Shorts', 'Skirt', 'Bottoms', 'Jeans', 'Pants']
CONSTANT_SHOES = ['Sneakers', 'Boots', 'Slippers', 'Flat', 'Sandals', 'Heels']
CONSTANT_TEMP_SEASON = ['Summer', 'Summer, Spring', 'Spring, Fall', 'Winter, Fall', 'Winter', 'Winter']
CONSTANT_TEMP_LEVEL = [[-10], [0], [10], [20], [30], [50]]
base_url = 'http://api.shopstyle.com/api/v2/products?pid=uid1856-40013684-44'


# Create your views here.
def home(request):
    return render(request, 'wowardrobe/index.html')


@login_required
def create(request):
    if request.method == 'GET':
        context = {"colors": CONSTANT_COLORS,
                   "category": CONSTANT_CATEGORY,
                   "event": CONSTANT_EVENT,
                   "brand": CONSTANT_BRAND,
                   "season": CONSTANT_SEASON,
                   "t_level": CONSTANT_TLEVEL,
                   "style": CONSTANT_STYLE,
                   "weather": CONSTANT_WEATHER
                   }
        return render(request, 'wowardrobe/create.html', context)
    elif request.method == 'POST' and 'clothes_id' in request.POST:
        context = {"colors": CONSTANT_COLORS,
                   "category": CONSTANT_CATEGORY,
                   "event": CONSTANT_EVENT,
                   "brand": CONSTANT_BRAND,
                   "season": CONSTANT_SEASON,
                   "t_level": CONSTANT_TLEVEL,
                   "style": CONSTANT_STYLE,
                   "weather": CONSTANT_WEATHER
                   }
        try:
            latest_clothes = Clothes.objects.get(id=request.POST['clothes_id'], user=request.user)
        except:
            return render(request, 'wowardrobe/create.html', context)
        if 'clothes_name' in request.POST:
            latest_clothes.name = request.POST['clothes_name']
        if 'color' in request.POST:
            list = request.POST.getlist('color')
            save_fields = ''
            for x in list:
                save_fields += x + ', '
                new_tag = Tags.objects.create(tagname=x, type='color', clothes=latest_clothes, user=request.user)
                new_tag.save()
            latest_clothes.color = save_fields[:-2]
        if 'brand' in request.POST:
            list = request.POST.getlist('brand')
            save_fields = ''
            for x in list:
                save_fields += x + ', '
                new_tag = Tags.objects.create(tagname=x, type='brand', clothes=latest_clothes, user=request.user)
                new_tag.save()
            latest_clothes.brand = save_fields[:-2]
        if 'category' in request.POST:
            list = request.POST.getlist('category')
            save_fields = ''
            isTop = False
            isBottom = False
            isShoes = False
            isDress = False
            isOutwear = False
            categoryType = ''
        for x in list:
            if not isTop and x in CONSTANT_TOPS or x == 'Top':
                if x != 'Top':
                    isTop = True
                categoryType = 'Top'
            elif not isOutwear and x in CONSTANT_OUTWEAR or x == 'Outwear':
                if x != 'Outwear':
                    isOutwear = True
                categoryType = 'Outwear'
            elif not isBottom and x in CONSTANT_BOTTOMS or x == 'Bottom':
                if x != 'Bottom':
                    isBottom = True
                categoryType = 'Bottom'
            elif not isShoes and x in CONSTANT_SHOES or x == 'Shoes':
                if isShoes != 'Shoes':
                    isShoes = True
                categoryType = 'Shoes'
            elif not isDress and x == 'Dress':
                isDress = True
                categoryType = 'Dress'
            save_fields += x + ', '
            new_tag = Tags.objects.create(tagname=x, type='subcategory', category=categoryType, clothes=latest_clothes, user=request.user)
            new_tag.save()
        if isTop:
            new_tag = Tags.objects.create(tagname='Top', type='category', clothes=latest_clothes, user=request.user)
            new_tag.save()
            save_fields += 'Top, '
        if isBottom:
            new_tag = Tags.objects.create(tagname='Bottom', type='category', clothes=latest_clothes, user=request.user)
            new_tag.save()
            save_fields += 'Bottom, '
        if isShoes:
            new_tag = Tags.objects.create(tagname='Shoes', type='category', clothes=latest_clothes, user=request.user)
            new_tag.save()
            save_fields += 'Shoes, '
        if isOutwear:
            new_tag = Tags.objects.create(tagname='Outwear', type='category', clothes=latest_clothes, user=request.user)
            new_tag.save()
            save_fields += 'Outwear, '
        latest_clothes.category = save_fields[:-2]
    if 'event' in request.POST:
        list = request.POST.getlist('event')
        save_fields = ''
        for x in list:
            save_fields += x + ', '
            new_tag = Tags.objects.create(tagname=x, type='event', clothes=latest_clothes, user=request.user)
            new_tag.save()
        latest_clothes.event = save_fields[:-2]
    if 'season' in request.POST:
        list = request.POST.getlist('season')
        save_fields = ''
        for x in list:
            save_fields += x + ', '
            new_tag = Tags.objects.create(tagname=x, type='season', clothes=latest_clothes, user=request.user)
            new_tag.save()
        latest_clothes.season = save_fields[:-2]
    if 'weather' in request.POST:
        list = request.POST.getlist('weather')
        save_fields = ''
        for x in list:
            save_fields += x + ', '
            new_tag = Tags.objects.create(tagname=x, type='weather', clothes=latest_clothes, user=request.user)
            new_tag.save()
        latest_clothes.weather = save_fields[:-2]
    if 'style' in request.POST:
        list = request.POST.getlist('style')
        save_fields = ''
        for x in list:
            save_fields += x + ', '
            new_tag = Tags.objects.create(tagname=x, type='style', clothes=latest_clothes, user=request.user)
            new_tag.save()
        latest_clothes.style = save_fields[:-2]
    if 'temp' in request.POST:
        latest_clothes.temperature_level = request.POST['temp']
        new_tag = Tags.objects.create(tagname=x, type='temp_level', clothes=latest_clothes, user=request.user)
        new_tag.save()
    latest_clothes.save()
    return render(request, 'wowardrobe/create.html', context)


@login_required
def mywardrobe(request):
    return render(request, 'wowardrobe/mywardrobe.html')


@login_required
def upload_clothes(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        # request.session['upload_file'] = uploaded_file
        content = base64.b64encode(uploaded_file.read()).decode("utf-8")
        post_data = {
            "requests": [{"image": {"content": content}, "features": [{"type": "LABEL_DETECTION", "maxResults": 10},
                                                                      {"type": "WEB_DETECTION", "maxResults": 10}]}]}
        encoded_data = json.dumps(post_data).encode('utf-8')
        http = urllib3.PoolManager()
        r = http.request('POST',
                         'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyCKny_zDjFjhLnc2Cd1QbkugYI5wbismws',
                         body=encoded_data, headers={"Content-Type": "application/json"})
        if r.status == 200:
            response = json.loads(r.data.decode('utf-8'))
            label_annotations = response["responses"][0]["labelAnnotations"]
            web_detections = response["responses"][0]["webDetection"]["webEntities"]
            colors = []
            categories = []
            events = []
            brands = []
            seasons = []
            weather = []
            styles = []
            temperature = []
            isCategoryRec = False
            for l in label_annotations:
                label = l["description"]
                if label.title() in CONSTANT_COLORS:
                    colors.append(label.title())
                if label.title() in CONSTANT_BRAND:
                    brands.append(label.title())
                if not isCategoryRec and (label.title() in CONSTANT_CATEGORY or label.title() == 'Boot'):
                    isCategoryRec = True
                    if label.title() == 'Boot':
                        categories.append('Boots')
                        label = 'Boots'
                    else:
                        categories.append(label.title())
                    if label.title() in DICT.keys():
                        key = label.title()
                        events = DICT[key][0]
                        seasons = DICT[key][1]
                        weather = DICT[key][2]
                        temperature = DICT[key][3]
                        styles = DICT[key][4]
                if label.title() in CONSTANT_EVENT:
                    events.append(label.title())

            if len(categories) == 0 and len(web_detections) > 0:
                for w in web_detections:
                    label = w["description"]
                    if label.title() in CONSTANT_COLORS:
                        colors.append(label.title())
                    if label.title() in CONSTANT_BRAND:
                        brands.append(label.title())
                    if not isCategoryRec and (label.title() in CONSTANT_CATEGORY or label.title() == 'Boot'):
                        isCategoryRec = True
                        if label.title() == 'Boot':
                            categories.append('Boots')
                            label = 'Boots'
                        else:
                            categories.append(label.title())
                        if label.title() in DICT.keys():
                            key = label.title()
                            events = DICT[key][0]
                            seasons = DICT[key][1]
                            weather = DICT[key][2]
                            temperature = DICT[key][3]
                            styles = DICT[key][4]
                    if label.title() in CONSTANT_EVENT:
                        events.append(label.title())

        context = {'colors': colors, 'categories': categories, 'events': events, 'brands': brands, 'seasons': seasons,
                   'weather': weather, 'temperature': temperature, 'styles': styles}

        new_clothes = Clothes.objects.create(image=uploaded_file, user=request.user)
        new_clothes.save()
        context['clothes_id'] = new_clothes.id
        messages.success(request, 'Clothes Saved Succesfully')
        return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def search_by_tags(request):
    if request.method == 'GET' and 'tags' in request.GET:
        tags = ''.join(request.GET['tags'])
        clothes = Clothes.objects.annotate(
            search=SearchVector('category', 'color', 'style', 'brand', 'event', 'weather', 'season')).filter(
            search=tags).filter(Q(user=request.user))
        context = {'clothes': clothes, "tags": tags}
        return render(request, 'wowardrobe/clothes.html', context)


@login_required
def search_outfits_by_tags(request):
    if request.method == 'GET' and 'tags' in request.GET:
        tags = ''.join(request.GET['tags'])
        outfits = Outfits.objects.annotate(
            search=SearchVector('name', 'season', 'event', 'style')).filter(
            search=tags).filter(Q(user=request.user))
        context = {'outfits': outfits, "tags": tags}
        return render(request, 'wowardrobe/outfits.html', context)


@login_required
def search_by_tags_outfit(request):
    if request.method == 'GET' and 'tags' in request.GET:
        tags = ''.join(request.GET['tags'])
        clothes_result = Clothes.objects.annotate(
            search=SearchVector('category', 'color', 'style', 'brand', 'event', 'weather', 'season')).filter(
            search=tags).filter(Q(user=request.user)).values('id', 'name', 'category', 'style', 'temperature_level')
        # json_res = str(json.dumps({'list_result': list(clothes_result)}))
        context = {'clothes_result': clothes_result}
        return JsonResponse({'results': list(clothes_result)}, safe=False)
        # return render(request, 'wowardrobe/results.json', context, content_type='application/json')


@login_required
def view_clothes_by_tag(request):
    tags = request.GET['tag']
    if '/' in tags:
        tag = tags.split('/')
        clothes = Clothes.objects.annotate(
            search=SearchVector('category', 'color', 'style', 'brand', 'event', 'weather', 'season')
        ).filter(search=SearchQuery(tag[0]) | SearchQuery(tag[1])).filter(Q(user=request.user))
    else:
        clothes = Clothes.objects.annotate(
            search=SearchVector('category', 'color', 'style', 'brand', 'event', 'weather', 'season')).filter(
            search=tags).filter(Q(user=request.user))
    context = {'clothes': clothes, "tags": tags}
    return render(request, 'wowardrobe/clothes.html', context)


@login_required
def view_outfits_by_tag(request):
    tags = request.GET['tag']
    if '/' in tags:
        tag = tags.split('/')
        outfits = Outfits.objects.annotate(
            search=SearchVector('event', 'style', 'season')
        ).filter(search=SearchQuery(tag[0]) | SearchQuery(tag[1])).filter(Q(user=request.user))
    else:
        outfits = Outfits.objects.annotate(
            search=SearchVector('event', 'style', 'season')).filter(
            search=tags).filter(Q(user=request.user))
    context = {'outfits': outfits, "tags": tags}
    return render(request, 'wowardrobe/outfits.html', context)


@login_required
def get_tags(request):
    if request.method == 'GET':
        tags = Tags.objects.filter(user=request.user).values_list('tagname', flat=True).distinct()
        data = json.dumps({'tags': list(tags)})
        return HttpResponse(data, content_type='application/json')
    return HttpResponse()


@login_required
def remove_clothes(request, id):
    try:
        clothes = Clothes.objects.get(id=id, user=request.user)
        clothes.delete()
    except ObjectDoesNotExist:
        redirect('/wowardrobe/mywardrobe')
    return redirect('/wowardrobe/mywardrobe')


@login_required
def get_image(request, id):
    entry = get_object_or_404(Clothes, id=id)
    if not entry.image:
        raise Http404

    content_type = guess_type(entry.image.name)
    return HttpResponse(entry.image, content_type=content_type)


def get_profile_image(request, user_id):
    entry = get_object_or_404(UserProfile, user_id=user_id)
    if not entry.image:
        raise Http404
    content_type = guess_type(entry.image.name)
    return HttpResponse(entry.image, content_type=content_type)


@login_required
def get_image_by_tag(request, tag):
    first_entry = get_object_or_404(Tags.objects.filter(tagname=tag, user=request.user).order_by('-id').first())
    entry = first_entry.clothes
    if not entry.image:
        raise Http404

    content_type = guess_type(entry.image.name)
    return HttpResponse(entry.image, content_type=content_type)


@login_required
def edit_clothes(request, id):
    try:
        clothes = Clothes.objects.get(id=id, user=request.user)
    except ObjectDoesNotExist:
        redirect('/wowardrobe/mywardrobe')
    if request.method == "GET":
        colors = clothes.color.split(",")
        brands = clothes.brand.split(",")
        events = clothes.event.split(",")
        categories = clothes.category.split(",")
        weathers = clothes.weather.split(",")
        seasons = clothes.season.split(",")
        styles = clothes.style.split(",")
        temp = clothes.temperature_level
        context = {
            'color': colors,
            'brand': brands,
            'event': events,
            'category': categories,
            'weather': weathers,
            'season': seasons,
            'style': styles,
            'temp': temp,
            'id': clothes.id,
            'name': clothes.name
        }
        return render(request, 'wowardrobe/edit.html', context)
    else:
        try:
            clothes_tags = Tags.objects.filter(clothes=clothes, user=request.user)
            clothes_tags.delete()
        except ObjectDoesNotExist:
            redirect('/wowardrobe/mywardrobe')
        if 'name' in request.POST:
            clothes.name = request.POST['name']
        if 'color' in request.POST:
            list = request.POST.getlist('color')
            save_fields = ''
            for x in list:
                save_fields += x + ', '
                new_tag = Tags.objects.create(tagname=x, type='color', clothes=clothes, user=request.user)
                new_tag.save()
                clothes.color = save_fields[:-2]
        if 'brand' in request.POST:
            list = request.POST.getlist('brand')
            save_fields = ''
            for x in list:
                save_fields += x + ', '
                new_tag = Tags.objects.create(tagname=x, type='brand', clothes=clothes, user=request.user)
                new_tag.save()
                clothes.brand = save_fields[:-2]
        if 'category' in request.POST:
            list = request.POST.getlist('category')
            save_fields = ''
            isTop = False
            isBottom = False
            isShoes = False
            isDress = False
            isOutwear = False
            categoryType = ''
            for x in list:
                if not isTop and x in CONSTANT_TOPS:
                    isTop = True
                    categoryType = 'Top'
                elif not isOutwear and x in CONSTANT_OUTWEAR:
                    isOutwear = True
                    categoryType = 'Outwear'
                elif not isBottom and x in CONSTANT_BOTTOMS:
                    isBottom = True
                    categoryType = 'Bottom'
                elif not isShoes and x in CONSTANT_SHOES:
                    isShoes = True
                    categoryType = 'Shoes'
                elif not isDress and x == 'Dress':
                    isDress = True
                    categoryType = 'Dress'
                save_fields += x + ', '
                new_tag = Tags.objects.create(tagname=x, type='subcategory', category=categoryType, clothes=clothes, user=request.user)
                new_tag.save()
                if isTop:
                    new_tag = Tags.objects.create(tagname='Top', type='category', clothes=clothes, user=request.user)
                    new_tag.save()
                    save_fields += 'Top, '
                if isBottom:
                    new_tag = Tags.objects.create(tagname='Bottom', type='category', clothes=clothes, user=request.user)
                    new_tag.save()
                    save_fields += 'Bottom, '
                if isOutwear:
                    new_tag = Tags.objects.create(tagname='Outwear', type='category', clothes=clothes, user=request.user)
                    new_tag.save()
                    save_fields += 'Outwear, '
                if isShoes:
                    new_tag = Tags.objects.create(tagname='Shoes', type='category', clothes=clothes, user=request.user)
                    new_tag.save()
                    save_fields += 'Shoes, '
                clothes.category = save_fields[:-2]
        if 'event' in request.POST:
            list = request.POST.getlist('event')
            save_fields = ''
            for x in list:
                save_fields += x + ', '
                new_tag = Tags.objects.create(tagname=x, type='event', clothes=clothes, user=request.user)
                new_tag.save()
                clothes.event = save_fields[:-2]
        if 'season' in request.POST:
            list = request.POST.getlist('season')
            save_fields = ''
            for x in list:
                save_fields += x + ', '
                new_tag = Tags.objects.create(tagname=x, type='season', clothes=clothes, user=request.user)
                new_tag.save()
                clothes.season = save_fields[:-2]
        if 'weather' in request.POST:
            list = request.POST.getlist('weather')
            save_fields = ''
            for x in list:
                save_fields += x + ', '
                new_tag = Tags.objects.create(tagname=x, type='weather', clothes=clothes, user=request.user)
                new_tag.save()
                clothes.weather = save_fields[:-2]
        if 'style' in request.POST:
            list = request.POST.getlist('style')
            save_fields = ''
            for x in list:
                save_fields += x + ', '
                new_tag = Tags.objects.create(tagname=x, type='style', clothes=clothes, user=request.user)
                new_tag.save()
                clothes.style = save_fields[:-2]
        if 'temp' in request.POST:
            clothes.temperature_level = request.POST['temp']
            new_tag = Tags.objects.create(tagname=x, type='temp_level', clothes=clothes, user=request.user)
            new_tag.save()
            clothes.save()
        return redirect('/wowardrobe/mywardrobe')


@transaction.atomic
def signin(request):
    context = {}
    if request.method == 'GET':
        context['form'] = AuthenticationForm(request.user)
        return render(request, 'wowardrobe/signin.html', context)


@transaction.atomic
def register(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'wowardrobe/signup.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'wowardrobe/signup.html', context)
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        password=form.cleaned_data['password1'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

    # profile = UserProfile(user = new_user,
    # 				  id = new_user.id,
    # 				  username = new_user.username,
    # 				  email=form.cleaned_data['email'],
    # 				  first_name=form.cleaned_data['first_name'],
    # 				  last_name=form.cleaned_data['last_name']
    # 				  )
    profile = UserProfile(user=new_user,
                          date_of_birth=form.cleaned_data['date_of_birth'],
                          gender=form.cleaned_data['gender'])
    profile.save()

    schedule = DailyOutfit(user=new_user)
    schedule.save()
    # profile_form = ProfileForm(request.POST,instance = request.user.profile)
    profile_form = CreateProfileForm(request.POST, instance=profile)

    token = default_token_generator.make_token(new_user)
    email_body = """
	Welcome to Grumblr. Please click the link below to
	verify your email address and complete the registration of your account:
	http://%s%s""" % (request.get_host(),
                      reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="dannil@andrew.cmu.edu",
              recipient_list=[new_user.email],
              )

    context['email'] = form.cleaned_data['email']
    return render(request, 'wowardrobe/needs_confirmation.html', context)


@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'wowardrobe/confirmed.html', {})


@login_required
def create_outfit(request):
    context = {"event": CONSTANT_EVENT,
               "season": CONSTANT_SEASON,
               "style": CONSTANT_STYLE,
               "weather": CONSTANT_WEATHER
               }
    clothes_outwears = Clothes.objects.filter(user=request.user, category__contains="Outwear")
    clothes_tops = Clothes.objects.filter(user=request.user, category__contains="Top")
    clothes_bottoms = Clothes.objects.filter(user=request.user, category__contains="Bottom")
    clothes_shoes = Clothes.objects.filter(user=request.user, category__contains="Shoes")
    clothes_dress = Clothes.objects.filter(user=request.user, category__contains="Dress")
    context["clothes_outwears"] = clothes_outwears
    context["clothes_tops"] = clothes_tops
    context["clothes_bottoms"] = clothes_bottoms
    context["clothes_shoes"] = clothes_shoes
    context["clothes_dress"] = clothes_dress
    return render(request, 'wowardrobe/create-outfit.html', context)


@login_required
def mylookbook(request):
    return render(request, 'wowardrobe/mylookbook.html')


@login_required
def daily_outfit(request):
    return render(request, 'wowardrobe/dailyoutfit.html')


@login_required
def upload_outfit(request):
    if request.method == 'POST':
        top1 = None
        top2 = None
        bottom = None
        dress = None
        shoes = None

        if 'top1' in request.POST and request.POST['top1']:
            top1Id = request.POST['top1']
            top1 = Clothes.objects.get(id=top1Id, user=request.user)
            top1 = top1
        if 'top2' in request.POST and request.POST['top2']:
            top2Id = request.POST['top2']
            top2 = Clothes.objects.get(id=top2Id, user=request.user)
            top2 = top2
        if 'bottom' in request.POST and request.POST['bottom']:
            bottomId = request.POST['bottom']
            bottom = Clothes.objects.get(id=bottomId, user=request.user)
            bottom = bottom
        if 'dress' in request.POST and request.POST['dress']:
            dressId = request.POST['dress']
            dress = Clothes.objects.get(id=dressId, user=request.user)
            dress = dress
        if 'shoes' in request.POST and request.POST['shoes']:
            shoesId = request.POST['shoes']
            shoes = Clothes.objects.get(id=shoesId, user=request.user)
            shoes = shoes

        if not Outfits.objects.filter(user = request.user,
                               top1 = top1,
                               top2 = top2,
                               bottom = bottom,
                               shoes = shoes,
                               dress = dress).exists():

            new_outfit = Outfits.objects.create(user = request.user,
                                            top1 = top1,
                                            top2 = top2,
                                            bottom = bottom,
                                            shoes = shoes,
                                            dress = dress)

            if 'temperature_level' in request.POST:
                level = int(request.POST['temperature_level'])
                new_outfit.temperature_level = level
            if 'styles' in request.POST:
                style = request.POST['styles']
                new_outfit.style = style
            if 'events' in request.POST:
                events = request.POST['events']
                new_outfit.event = events
            if 'seasons' in request.POST:
                seasons = request.POST['seasons']
                new_outfit.season = seasons
            if 'name' in request.POST:
                name = request.POST['name']
                new_outfit.name = name
            new_outfit.save()
    return HttpResponse()


@login_required
def get_overview(request):
    return render(request, 'wowardrobe/overview.html', {})


@login_required
def get_category_count(request):
    category_count = Tags.objects.filter(user=request.user).values('category').annotate(count=Count('id')).order_by('-count')
    return JsonResponse(list(category_count), safe=False)


@login_required
def get_tops_count(request):
    top_subcategories = Tags.objects.filter(type='subcategory', category='Top', user=request.user).values('tagname').annotate(
        count=Count('id')).order_by('-count')
    return JsonResponse(list(top_subcategories), safe=False)


@login_required
def get_bottoms_count(request):
    bottom_subcategories = Tags.objects.filter(type='subcategory', category='Bottom', user=request.user).values('tagname').annotate(
        count=Count('id')).order_by('-count')
    return JsonResponse(list(bottom_subcategories), safe=False)


@login_required
def get_shoes_count(request):
    shoes_subcategories = Tags.objects.filter(type='subcategory', category='Shoes', user=request.user).values('tagname').annotate(
        count=Count('id')).order_by('-count')
    return JsonResponse(list(shoes_subcategories), safe=False)


@login_required
def get_color_count(request):
    colors = Tags.objects.filter(type='color', user=request.user).values('tagname').annotate(count=Count('id')).order_by('-count')
    return JsonResponse(list(colors), safe=False)


@login_required
def get_brand_count(request):
    brands = Tags.objects.filter(type='brand', user=request.user).values('tagname').annotate(count=Count('id')).order_by('-count')
    return JsonResponse(list(brands), safe=False)


@login_required
def get_style_count(request):
    styles = Tags.objects.filter(type='style', user=request.user).values('tagname').annotate(count=Count('id')).order_by('-count')
    return JsonResponse(list(styles), safe=False)


@login_required
def get_season_count(request):
    seasons = Tags.objects.filter(type='season', user=request.user).values('tagname').annotate(count=Count('id')).order_by('-count')
    return JsonResponse(list(seasons), safe=False)


@login_required
def get_event_count(request):
    events = Tags.objects.filter(type='event', user=request.user).values('tagname').annotate(count=Count('id')).order_by('-count')
    return JsonResponse(list(events), safe=False)


@login_required
def get_style_tags(request):
    if request.method == 'GET':
        tags = Tags.objects.filter(type='style', user=request.user).values_list('tagname', flat=True).distinct()
        return JsonResponse(list(tags), safe=False)
    return HttpResponse()


@login_required
def get_event_tags(request):
    if request.method == 'GET':
        tags = Tags.objects.filter(type='event', user=request.user).values_list('tagname', flat=True).distinct()
        return JsonResponse(list(tags), safe=False)
    return HttpResponse()


@login_required
def get_recommendation(request):
    context = {}
    return render(request, 'wowardrobe/recommendation.html', context)


@login_required
def get_recommendation_by_params(request):
    if request.method == 'GET':
        context = {}
        event = ''
        style = ''
        weather = ''
        day = ''
        if 'day' in request.GET and request.GET['day']:
            day = request.GET['day']
            if day == 'today':
                if 'weatherCode1' in request.GET and request.GET['weatherCode1']:
                    weatherContext = request.GET['weatherCode1']
            elif day == 'tomorrow':
                if 'weatherCode2' in request.GET and request.GET['weatherCode2']:
                    weatherContext = request.GET['weatherCode2']
            context['day'] = day
            temp_arr = weatherContext.split(',')
            weatherCode = float(temp_arr[0])
            temp_min = float(temp_arr[1])
            temp_max = float(temp_arr[2])
            if temp_min < -10:
                temp_level1 = 6
            elif temp_min < 0:
                temp_level1 = 5
            else:
                temp_level1 = 4 - round(temp_min / 10)
            if temp_max > 30:
                temp_level2 = 1
            elif temp_max < 0:
                temp_level2 = 5
            else:
                temp_level2 = 4 - round(temp_max / 10)
        if 'event' in request.GET and request.GET['event']:
            event = ','.join(request.GET['event'])
        if 'style' in request.GET and request.GET['style']:
            style = ','.join(request.GET['style'])
        if weatherCode >= 200 and weatherCode < 600:
            weather = 'Rainy'
        elif weatherCode >= 600 and weatherCode < 800:
            weather = 'Snowy'
        elif weatherCode == 800:
            weather = 'Sunny'
        elif weatherCode > 800 and weatherCode < 900:
            weather = 'Cloudy'
        elif weatherCode >= 900:
            weather = 'Windy'
        now = datetime.datetime.now()
        month = now.month
        season = ''
        if month in [3, 5]:
            season = 'Spring'
        elif month in [6, 8]:
            season = 'Summer'
        elif month in [9, 11]:
            season = 'Fall'
        else:
            season = 'Winter'
        query_tags = style + ',' + event + ',' + weather + ',' + season
        outfits = Outfits.objects.annotate(
            search=SearchVector('event', 'style', 'season')).filter(
            search=query_tags).filter((Q(temperature_level=temp_level1) | Q(temperature_level=temp_level2)) & Q(user=request.user))
        if len(outfits) > 0:
            if len(outfits) > 1:
                random_index = randint(0, len(outfits) - 1)
                outfit = list(outfits)[random_index]
            elif len(outfits) == 1:
                outfit = list(outfits)[0]
            top1 = outfit.top1
            top2 = outfit.top2
            bottom = outfit.bottom
            dress = outfit.dress
            shoes = outfit.shoes
            context['dress'] = dress
            context['top2'] = top2
            context['shoes'] = shoes
            context['top1'] = top1
            context['bottom'] = bottom
        else:
            # Get tops
            random_num = randint(0, 2)

            top1 = get_recom_clothes(style, event, weather, season, temp_level1, temp_level2, 'Top', request.user)
            if type(top1) == int:
                return render(request, 'wowardrobe/clothes_error.json', context, content_type='application/json')
            context['top1'] = top1
            if temp_level1 >= 2:
                top2 = get_recom_clothes(style, event, weather, season, temp_level1, temp_level2, 'Outwear', request.user)
                if type(top2) == int:
                    return render(request, 'wowardrobe/clothes_error.json', context, content_type='application/json')
                context['top2'] = top2

            # Get bottoms
            bottom = get_recom_clothes(style, event, weather, season, temp_level1, temp_level2, 'Bottom', request.user)
            context['bottom'] = bottom
            if type(bottom) == int:
                return render(request, 'wowardrobe/clothes_error.json', context, content_type='application/json')
            context['bottom'] = bottom

            # Get shoes
            shoes = get_recom_clothes(style, event, weather, season, temp_level1, temp_level2, 'Shoes', request.user)
            if type(shoes) == int:
                return render(request, 'wowardrobe/clothes_error.json', context, content_type='application/json')
            context['shoes'] = shoes

            # Get dress
            dress = get_recom_clothes(style, event, weather, season, temp_level1, temp_level2, 'Dress', request.user)
            if type(dress) != int and random_num == 1:
                context['dress'] = dress
                context.pop('top1', None)
                context.pop('bottom', None)
    return render(request, 'wowardrobe/recommendation.json', context, content_type='application/json')


def get_recom_clothes(style, event, weather, season, temp_level1, temp_level2, category, user):
    # search event, style, weather, season, temp
    query_tags = style + ',' + event + ',' + weather + ',' + season
    query_clothes = query_tags + ',' + category
    recom_clothes = Clothes.objects.annotate(
        search=SearchVector('category', 'event', 'style', 'weather', 'season')).filter(
        search=query_clothes).filter((Q(temperature_level=temp_level1) | Q(temperature_level=temp_level2)) & Q(user=user))
    if len(recom_clothes) > 1:
        random_index = randint(0, len(recom_clothes) - 1)
        recommend = list(recom_clothes)[random_index]
        return recommend
    elif len(recom_clothes) == 1:
        recommend = list(recom_clothes)[0]
        return recommend
    else:
        if style != '':
            # search event, weather, season, temp
            query_tags = event + ',' + weather + ',' + season
            query_clothes = query_tags + ',' + category
            recom_clothes = Clothes.objects.annotate(
                search=SearchVector('category', 'event', 'weather', 'season')).filter(
                search=query_clothes).filter((Q(temperature_level=temp_level1) | Q(temperature_level=temp_level2)) & Q(user=user))
            if len(recom_clothes) > 1:
                random_index = randint(0, len(recom_clothes) - 1)
                recommend = list(recom_clothes)[random_index]
                return recommend
            elif len(recom_clothes) == 1:
                recommend = list(recom_clothes)[0]
                return recommend

        if event != '':
            # search event, temp
            query_tags = event
            query_clothes = query_tags + ',' + category
            recom_clothes = Clothes.objects.annotate(
                search=SearchVector('category', 'event')).filter(
                search=query_clothes).filter(
                (Q(temperature_level=temp_level1) | Q(temperature_level=temp_level2)) & Q(user=user))
            if len(recom_clothes) > 1:
                random_index = randint(0, len(recom_clothes) - 1)
                recommend = list(recom_clothes)[random_index]
                return recommend
            elif len(recom_clothes) == 1:
                recommend = list(recom_clothes)[0]
                return recommend
            else:
                # event
                query_tags = event
                query_clothes = query_tags + ',' + category
                recom_clothes = Clothes.objects.annotate(
                    search=SearchVector('category', 'event')).filter(
                    search=query_clothes).filter(Q(user=user))
                if len(recom_clothes) > 1:
                    random_index = randint(0, len(recom_clothes) - 1)
                    recommend = list(recom_clothes)[random_index]
                    return recommend
                elif len(recom_clothes) == 1:
                    recommend = list(recom_clothes)[0]
                    return recommend

        # search temp
        query_clothes = category
        recom_clothes = Clothes.objects.annotate(
            search=SearchVector('category')).filter(
            search=query_clothes).filter(
            (Q(temperature_level=temp_level1) | Q(temperature_level=temp_level2)) & Q(user=user))
        if len(recom_clothes) > 1:
            random_index = randint(0, len(recom_clothes) - 1)
            recommend = list(recom_clothes)[random_index]
        elif len(recom_clothes) == 1:
            recommend = list(recom_clothes)[0]
        else:
            recommend = Clothes.random(Clothes, category, user)
    return recommend


@login_required
def get_clothes_by_budget(request):
    context = {"category": CONSTANT_CATEGORY,
               "brand": get_top_n_brand(10, request.user),
               "colors": get_top_n_color(10, request.user),
               'categoryTags': [],
               'brandTags': [],
               'colorTags': []
               }
    query_str = base_url
    profile = UserProfile.objects.get(user=request.user)
    if profile.gender == 'M':
        gender = 'man'
    else:
        gender = 'woman'

    params = {}

    if request.method == 'POST':
        fav_brand = ''
        fav_color = ''
        if 'category' in request.POST and request.POST['category']:
            categories = ''.join(request.POST.getlist('category'))
            params['fts'] = categories
            context['categoryTags'] = request.POST.getlist('category')
        if 'brand' in request.POST and request.POST['brand']:
            brands = ''.join(request.POST.getlist('brand'))
            brands = brands.replace('&', '-').replace(' ', '-')
            params['b'] = brands
            context['brandTags'] = request.POST.getlist('brand')
        else:
            fav_brand = get_top_n_brand(1, request.user)
        if 'color' in request.POST and request.POST['color']:
            colors = ''.join(request.POST.getlist('color'))
            params['c'] = colors
            context['colorTags'] = request.POST.getlist('color')
        else:
            fav_color = get_top_n_color(1, request.user)
        if 'budget' in request.POST and request.POST['budget']:
            max_price = request.POST['budget']
            params['max-price'] = max_price
            context['budget'] = request.POST['budget']

    params['offset'] = '0'
    params['limit'] = '10'
    encodeUrl = urlencode(params)
    query_str = query_str + "&" + encodeUrl
    http = urllib3.PoolManager()
    r = http.request('GET',
                     query_str, headers={"Content-Type": "application/json"})
    if r.status == 200:
        response = json.loads(r.data.decode('utf-8'))
        products = response['products']
        if len(products) == 0:
            query_str = base_url + '&fts='
            params = ''
            if 'brand' in request.POST and request.POST['brand']:
                brands = ''.join(request.POST['brand'])
                brands = brands.replace('&', '-').replace(' ', '+')
                params = params + '+' + brands
            if 'color' in request.POST and request.POST['color']:
                colors = '+'.join(request.POST['color'])
                params = params + '+' + colors
            if 'category' in request.POST and request.POST['category']:
                categories = '+'.join(request.POST['category'])
                params = params + '+' + categories
            if 'budget' in request.POST and request.POST['budget']:
                max_price = request.POST['budget']
                params = params + '&max-price=' + max_price
            query_str = query_str + params + '&offset=0&limit=10'
            r = http.request('GET',
                             query_str, headers={"Content-Type": "application/json"})
            if r.status == 200:
                response = json.loads(r.data.decode('utf-8'))
                products = response.products
                if len(products) == 0:
                    context["error"] = "No results found!"
                    return render(request, 'wowardrobe/expand.html', context)
        recommend_prods = []
        if len(products) <= 4:
            for p in products:
                recommend_prods.append({
                    'name': p['name'],
                    'price': p['priceLabel'],
                    'imageUrl': p['image']['sizes']['Best']['url'],
                    'clickUrl': p['clickUrl']
                })
        else:
            if fav_color != '' or fav_brand != '':
                if 'c' not in params:
                    params['c'] = fav_color[0]
                if 'b' not in params:
                    params['b'] = fav_brand[0].replace('&', '-')
                encodeUrl = urlencode(params)
                query_str = query_str + "&" + encodeUrl
                http = urllib3.PoolManager()
                r = http.request('GET',
                                 query_str, headers={"Content-Type": "application/json"})
                if r.status == 200:
                    response = json.loads(r.data.decode('utf-8'))
                    fav_products = response['products']
                    if len(fav_products) > 0:
                        index = randint(0, len(fav_products) - 1)
                        p = fav_products[index]
                        prod = {}
                        prod['name'] = p['name']
                        prod['price'] = p['priceLabel']
                        prod['imageUrl'] = p['image']['sizes']['Best']['url']
                        prod['clickUrl'] = p['clickUrl']
                        recommend_prods.append(prod)

            index = randint(0, len(products) - 1)
            length = 5
            if len(recommend_prods) > 0:
                length = 4
            for i in range(1, length):
                index = index % len(products)
                p = products[index]
                prod = {}
                prod['name'] = p['name']
                prod['price'] = p['priceLabel']
                prod['imageUrl'] = p['image']['sizes']['Best']['url']
                prod['clickUrl'] = p['clickUrl']
                recommend_prods.append(prod)
                index = index + 1
        context['data'] = recommend_prods
        return render(request, 'wowardrobe/expand.html', context)
    return render(request, 'wowardrobe/expand.html', context)


@login_required
@transaction.atomic
def edit_profile(request):
    context = {}
    try:
        profile_to_edit = UserProfile.objects.get(user=request.user)
    except:
        return render(request, 'wowardrobe/edit_profile.html')

    if request.method == "GET":
        form = EditProfileForm(instance=profile_to_edit)  # Create form from the exisitng profile
        context = {'form': form}
        return render(request, 'wowardrobe/edit_profile.html', context)

    profile_to_edit = UserProfile.objects.select_for_update().get(user=request.user)
    form = EditProfileForm(request.POST, request.FILES, instance=profile_to_edit)

    if not form.is_valid():
        context['form'] = form
        context = {'profile': profile_to_edit, 'form': form}
        return render(request, 'wowardrobe/edit_profile.html', context)
    else:
        profile_to_edit.content_type = form.cleaned_data['image'].content_type
        form.save()
        context = {
            'message': 'Profile Updated',
            'profile': profile_to_edit,
            'form': form,
        }
    return render(request, 'wowardrobe/edit_profile.html', context)


@login_required
def expand_wardrobe(request):
    context = {"category": CONSTANT_CATEGORY,
               "brand": get_top_n_brand(10, request.user),
               "colors": get_top_n_color(10, request.user)
               }
    return render(request, 'wowardrobe/expand.html', context)


def get_top_n_brand(n, user):
    brands = Tags.objects.filter(type='brand', user=user).values('tagname').annotate(count=Count('id')).order_by('-count')[
             :n].values_list('tagname', flat=True)
    return list(brands)


def get_top_n_color(n, user):
    colors = Tags.objects.filter(type='color', user=user).values('tagname').annotate(count=Count('id')).order_by('-count')[
             :n].values_list('tagname', flat=True)
    return list(colors)


@login_required
def save_outfit_to_schedule(request):
    context={}

    if request.method == 'POST':
        styles = {}
        events = {}
        temperature = {}
        top1 = None
        top2 = None
        bottom = None
        dress = None
        shoes = None
        if 'top1' in request.POST and request.POST['top1']:
            top1Id = request.POST['top1']
            top1 = Clothes.objects.get(id=top1Id, user=request.user)
            top1_events = top1.event.split(',')
            if len(top1_events) > 0:
                for e in top1_events:
                    if e in events:
                        events[e] = events[e] + 1
                    else:
                        events[e] = 1
            if top1.temperature_level > -1:
                if top1.temperature_level in temperature:
                    temperature[top1.temperature_level] = temperature[top1.temperature_level] + 1
                else:
                    temperature[top1.temperature_level] = 1
            top1_styles = top1.style.split(',')
            for s in top1_styles:
                if len(s) > 0:
                    if s in styles:
                        styles[s] = styles[s] + 1
                    else:
                        styles[s] = 1

        if 'top2' in request.POST and request.POST['top2']:
            top2Id = request.POST['top2']
            top2 = Clothes.objects.get(id=top2Id, user=request.user)
            top2_events = top2.event.split(',')
            if len(top2_events) > 0:
                for e in top2_events:
                    if e in events:
                        events[e] = events[e] + 1
                    else:
                        events[e] = 1
            if top2.temperature_level > 0:
                if top2.temperature_level in temperature:
                    temperature[top2.temperature_level] = temperature[top2.temperature_level] + 1
                else:
                    temperature[top2.temperature_level] = 1
            top2_styles = top2.style.split(',')
            for s in top2_styles:
                if len(s) > 0:
                    if s in styles:
                        styles[s] = styles[s] + 1
                    else:
                        styles[s] = 1
        if 'bottom' in request.POST and request.POST['bottom']:
            bottomId = request.POST['bottom']
            bottom = Clothes.objects.get(id=bottomId, user=request.user)
            bottom_events = bottom.event.split(',')
            if len(bottom_events) > 0:
                for e in bottom_events:
                    if e in events:
                        events[e] = events[e] + 1
                    else:
                        events[e] = 1
            if bottom.temperature_level > 0:
                if bottom.temperature_level in temperature:
                    temperature[bottom.temperature_level] = temperature[bottom.temperature_level] + 1
                else:
                    temperature[bottom.temperature_level] = 1
            bottom_styles = bottom.style.split(',')
            for s in bottom_styles:
                if len(s) > 0:
                    if s in styles:
                        styles[s] = styles[s] + 1
                    else:
                        styles[s] = 1
        if 'dress' in request.POST and request.POST['dress']:
            dressId = request.POST['dress']
            dress = Clothes.objects.get(id=dressId, user=request.user)
            dress_events = dress.event.split(',')
            if len(dress_events) > 0:
                for e in dress_events:
                    if e in events:
                        events[e] = events[e] + 1
                    else:
                        events[e] = 1
            if dress.temperature_level > 0:
                if dress.temperature_level in temperature:
                    temperature[dress.temperature_level] = temperature[dress.temperature_level] + 1
                else:
                    temperature[dress.temperature_level] = 1
            dress_styles = dress.style.split(',')
            for s in dress_styles:
                if len(s) > 0:
                    if s in styles:
                        styles[s] = styles[s] + 1
                    else:
                        styles[s] = 1
        if 'shoes' in request.POST and request.POST['shoes']:
            shoesId = request.POST['shoes']
            shoes = Clothes.objects.get(id=shoesId, user=request.user)
            shoes_events = shoes.event.split(',')
            if len(shoes_events) > 0:
                for e in shoes_events:
                    if e in events:
                        events[e] = events[e] + 1
                    else:
                        events[e] = 1
            if shoes.temperature_level > 0:
                if shoes.temperature_level in temperature:
                    temperature[shoes.temperature_level] = temperature[shoes.temperature_level] + 1
                else:
                    temperature[shoes.temperature_level] = 1
            shoes_styles = shoes.style.split(',')
            for s in shoes_styles:
                if len(s) > 0:
                    if s in styles:
                        styles[s] = styles[s] + 1
                    else:
                        styles[s] = 1
        if Outfits.objects.filter(user = request.user,
                               top1 = top1,
                               top2 = top2,
                               bottom = bottom,
                               shoes = shoes,
                               dress = dress).exists():
            new_outfit = Outfits.objects.get(user = request.user,
                               top1 = top1,
                               top2 = top2,
                               bottom = bottom,
                               shoes = shoes,
                               dress = dress)
        else:
            new_outfit = Outfits.objects.create(user = request.user,
                                            top1 = top1,
                                            top2 = top2,
                                            bottom = bottom,
                                            shoes = shoes,
                                            dress = dress)
        sorted_events = sorted(events.items(), key=operator.itemgetter(1), reverse=True)
        length = min(len(sorted_events), 5)
        events_tags = ''
        for x in range(0, length - 1):
            events_tags = events_tags + sorted_events[x][0] + ','
        new_outfit.event = events_tags[:-1]

        sorted_styles = sorted(styles.items(), key=operator.itemgetter(1), reverse=True)
        styles_tags = ''
        length = min(len(sorted_styles), 5)
        for x in range(0, length - 1):
            styles_tags = styles_tags + sorted_styles[x][0] + ','
        new_outfit.style = styles_tags[:-1]

        sorted_temp = sorted(temperature.items(), key=operator.itemgetter(1), reverse=True)
        if len(sorted_temp) > 0:
            if sorted_temp[0][0] >= 1 and sorted_temp[0][0] <= 5:
                new_outfit.temperature_level = sorted_temp[0][0] + 1
            else:
                new_outfit.temperature_level = sorted_temp[0][0]

        seasons = CONSTANT_TEMP_SEASON[new_outfit.temperature_level - 1]
        new_outfit.season = seasons
        new_outfit.save()
        try:
            new_schedule = DailyOutfit.objects.get(user=request.user)
        except ObjectDoesNotExist:
            new_schedule = DailyOutfit.objects.create(user=request.user)
        if 'schedule_day' in request.POST:
            day = request.POST['schedule_day']
            if day == 'today':
                new_schedule.today = new_outfit
            elif day == 'tomorrow':
                new_schedule.tomorrow = new_outfit
        new_schedule.save()

        context = {'schedule': new_schedule}
    return render(request, 'wowardrobe/dailyoutfit.html', context)


@login_required
def view_schedule(request):
    try:
        new_schedule = DailyOutfit.objects.get(user=request.user)
        context = {'schedule': new_schedule}
    except ObjectDoesNotExist:
        return render(request, 'wowardrobe/dailyoutfit.html')
    return render(request, 'wowardrobe/dailyoutfit.html', context)


def handler404(request):
    return render(request, 'wowardrobe/404.html', status=404)

def handler500(request):
    return render(request, 'wowardrobe/500.html', status=404)

@login_required
def edit_outfit(request,id):
    try:
        outfit = Outfits.objects.get(id=id, user=request.user)
    except ObjectDoesNotExist:
        redirect('/wowardrobe/mylookbook')
    if request.method == "GET":
        context = {'outfit': outfit,
                   'event': outfit.event.split(","),
                   'style': outfit.style.split(","),
                   'season':outfit.season.split(','),
                   'temp': outfit.temperature_level}
        return render(request, 'wowardrobe/edit_outfit.html', context)

@login_required
def remove_outfit(request,id):
    try:
        outfit = Outfits.objects.get(id=id, user=request.user)
        outfit.delete()
    except ObjectDoesNotExist:
        redirect('/wowardrobe/mylookbook')
    return redirect('/wowardrobe/mylookbook')

@login_required
def view_profile(request):
    myprofile = UserProfile.objects.get(user = request.user)
    context = {'profile':myprofile}
    return render(request,'wowardrobe/view_profile.html',context)
