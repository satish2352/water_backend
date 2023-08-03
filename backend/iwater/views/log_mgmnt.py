
from django.http.response import JsonResponse

from rest_framework.decorators import api_view

from init_water_app.settings import LOG_FILE_LOCATION


def get_logfile_data(filename, lines, count, n):
    with open(filename) as file:
        for line in file:
            line = line.strip()  # or some other preprocessing
            lines.append(line)  # storing everything in memory!
            if "continued from:" in line:
                oldfile = line.split(':')[2]
                get_logfile_data(oldfile, lines, count, n)
            count += 1
            if count > n:
                lines.append("...")
                return lines
    return lines


def get_logfile(n=1000):
    lines = []
    count = 0
    return get_logfile_data(LOG_FILE_LOCATION, lines, count, n)


@api_view(['GET'])
def get_log(request, n):
    return JsonResponse(get_logfile(n), safe=False)
