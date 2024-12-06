from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

# Create your views here.
def events(request):
    return render(request, 'event/events.html')


# def scrape():
#     url = "https://gdg.community.dev/gdg-on-campus-prathyusha-engineering-college-thiruvallur-india/"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     data = soup.find(id="taz9mL2u80T")
#     print(data.text)

# scrape()


