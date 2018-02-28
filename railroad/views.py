from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def keyboard(request):
    return JsonResponse(
        {
            'type':'buttons',
            'buttons':['여객열차 조회','화물열차 조회','오늘의 갑종']
        }
    )

@csrf_exempt
def message(request):
    json_str = (request.body).decode('utf-8')
    received_json = json.loads(json_str)
    content = received_json['content']
    return JsonResponse
    (
        {
            'message':{'text':content},
            'keyboard':{'type':'buttons','buttons':['여객열차 조회','화물열차 조회','오늘의 갑종']}
        }
    )
