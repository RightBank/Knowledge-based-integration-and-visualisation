from django.http import HttpResponse, JsonResponse
from .data_fetch_and_wrapping import data_fetch, legend_info_fetch
from .data_update import data_update
from django.shortcuts import render


def web_map(request):
    wrapped_data = data_fetch()
    # return HttpResponse(wrapped_data)
    if request.GET:
        phenomenon = str(request.GET['phenomenon'])
        # print(phenomenon)
        data_update(phenomenon)
        wrapped_data = data_fetch()
        wrapped_data.append(legend_info_fetch())
        return JsonResponse(wrapped_data, safe=False)

    data = {'data': str('')}
    return render(request, r'kb_cycling/index.html', data)