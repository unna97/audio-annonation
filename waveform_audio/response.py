from django.http import HttpResponse


def generate_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    response.write('some text')
    return response

