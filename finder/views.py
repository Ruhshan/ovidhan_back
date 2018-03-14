from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
#search word imports
import urllib3
import urllib.parse
from bs4 import BeautifulSoup
import json

http = urllib3.PoolManager()
# Create your views here.


def search_word(query):
    encoded_word = urllib.parse.quote_plus(query)
    url = 'http://www.english-bangla.com/bntobn/index/' + encoded_word
    response = http.request('GET', url)

    soup = BeautifulSoup(response.data, "html.parser")

    w_info = soup.find("div", {"id": "w_info"})
    try:
        stl3 = w_info.find("span", {"class":"stl3"})
        format1 = w_info.find("span", {"class":"format1"})
    except:
        stl3 = stl3 = '<span class="stl3" style="font-family:SolaimanLipi, TonnyBanglaMJ,  Times, serif"> {}</span>'.format(query)
        format1 = '<span class="format1" style="font-family:SolaimanLipi, TonnyBanglaMJ,  Times, serif"> শব্দটি পাওয়া যায়নি </span>'

    result = {'query':str(stl3), 'meaning':str(format1)}
    print(json.dumps(result))
    return result


class FindView(View):
    def get(self, request):
        query_word = request.GET['query']
        search_result = search_word(query_word)

        return HttpResponse(json.dumps(search_result))


