from .models import *

def is_staff(request):
    user_id = request.session.get('user_id')
    print(user_id)
    user = UserProfile.objects.get(pk=user_id)
    if user.role!='Student':
        return {'is_staff':True}
    return {'is_staff':False}