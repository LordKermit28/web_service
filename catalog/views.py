from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def information_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(name, phone, message)
    return render(request, 'main/information.html')
