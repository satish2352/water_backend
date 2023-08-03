# from django.shortcuts import redirect
# from django.urls import reverse

# class BlockMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             print("middlew")
#             if request.user.is_blocked:
#                 print('blokced')
#                 if request.path != reverse('blocked'):
#                     return redirect('blocked')
#         response = self.get_response(request)
#         return response
