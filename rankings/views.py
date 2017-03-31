from django.shortcuts import render

# Create your views here.

def statistics(request):
    context = {
        'title': 'Rankings e Estatísticas',
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Rankings'},
        ],
        "teste": 21
    }
    return render(request, 'rankings.html', context)