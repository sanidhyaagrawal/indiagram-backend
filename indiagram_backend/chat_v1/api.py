from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import MessageModelSerializer, UserModelSerializer
from .models import MessageModel, likedStream, lastSeen

from api_v1.views import keyisValid, usernameisValid
from api_v1.models import user_details

from django.views.decorators.csrf import csrf_exempt

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



@api_view(['POST'])
def messageSeen(request): 
    if request.method == 'POST':
        data = request.data
        if data.get('key') == None or data.get('target') == None or data.get('upto_id') == None:
            return Response({'error': "Invalid body parameter, body must contain 'key', 'target' and 'upto_id'"}, status=status.HTTP_400_BAD_REQUEST)
        
        key = data.get('key')
        upto_id = data.get('upto_id')
        target = data.get('target')

        keyValid, user = keyisValid(key)
        usernameValid, recipient = usernameisValid(target)
        if keyValid and usernameValid:   
            msgs = MessageModel.objects.all().filter(Q(recipient=recipient, user=user) | Q(user=recipient, recipient=user)).filter(pk__lte=upto_id, seen = False).order_by('pk')
            #print(msgs)
            for msg in msgs:
                msg.seen = True
                msg.save()

            notification = {
                'type': 'push_seen',
                'chat': user.username,
                'seen': True,
                'upto_id': '{}'.format(upto_id)
            }
            channel_layer = get_channel_layer()
            #async_to_sync(channel_layer.group_send)("{}".format(user.username), notification)
            async_to_sync(channel_layer.group_send)("{}".format(recipient.username), notification)

            return Response(status=status.HTTP_202_ACCEPTED)
        else:   
            return Response({'error_header':'Something went wrong','error_body': "Something went wrong, please try again later.", "actions": [{"error_code": "1001", 'error_message': 'Try Again'}]}, status=status.HTTP_200_OK)

@api_view(['POST'])
def messageLike(request): 
    if request.method == 'POST':
        data = request.data
        if data.get('key') == None or data.get('messageID') == None or data.get('liked') == None:
            return Response({'error': "Invalid body parameter, body must contain 'key', 'liked' and 'messageID'"}, status=status.HTTP_400_BAD_REQUEST)
        
        key = data.get('key')
        messageID = data.get('messageID')
        liked = data.get('liked')

        keyValid, user = keyisValid(key)
        if keyValid:
            try:   
                msg = MessageModel.objects.get(Q(user=user, pk=messageID) | Q(recipient=user, pk=messageID))
            except:
                return Response({'error_header':'Message not found','error_body': "No such message exists or you are not authorised to access this message.", "actions": [{"error_code": "1001", 'error_message': 'Understood'}]}, status=status.HTTP_200_OK)

            #print(msg)
            if liked == "True" or liked == True or liked == 1 or liked == "1": 
                msg.liked = True
                msg.save()
                obj, created = likedStream.objects.update_or_create(message=msg, defaults={"message": msg, "user":user, "state":True},)
                #print(obj, created)
            else:
                msg.liked = False
                msg.save()     
                obj, created = likedStream.objects.update_or_create(message=msg, defaults={"message": msg, "user":user, "state":False},)
                #print(obj, created)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:   
            return Response({'error_header':'Something went wrong','error_body': "Something went wrong, please try again later.", "actions": [{"error_code": "1001", 'error_message': 'Try Again'}]}, status=status.HTTP_200_OK)




@api_view(['POST'])
def chatHistory(request): 
    #using seek pagation. page_size = 15
    if request.method == 'POST':
        data = request.data
        if data.get('key') == None or data.get('target') == None:
            return Response({'error': "Invalid body parameter, body must contain 'key' and 'target' with optional arguments 'limit' and 'before_id'"}, status=status.HTTP_400_BAD_REQUEST)
        key = data.get('key')
        target = data.get('target')
        
        page_size = 30 #IMP_CONSTANT

        if data.get('limit') == None:
            limit = page_size
        else:
            limit = int(data.get('limit'))
            if limit > page_size:
                limit = page_size
        if data.get('before_id') == None:
            before_id = False 
        else:
            before_id = int(data.get('before_id'))

        keyValid, user = keyisValid(key)
        usernameValid, recipient = usernameisValid(target)
        if keyValid and usernameValid:   
            if before_id == False:
                msg = MessageModel.objects.all().filter(Q(recipient=recipient, user=user) | Q(user=recipient, recipient=user)).order_by('-pk')[:limit:-1]
            else:
                msg = MessageModel.objects.all().filter(Q(recipient=recipient, user=user) | Q(user=recipient, recipient=user)).filter(pk__lt=before_id).order_by('-pk')[:limit:-1]

            serializer = MessageModelSerializer(msg, many = True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:   
            return Response({'error_header':'Something went wrong','error_body': "Something went wrong, please try again later.", "actions": [{"error_code": "1001", 'error_message': 'Try Again'}]}, status=status.HTTP_200_OK)



@api_view(['POST'])
def getMessage(request): 
    if request.method == 'POST':
        data = request.data
        if data.get('key') == None or data.get('messageID') == None:
            return Response({'error': "Invalid body parameter, body must contain 'key' and 'messageID'"}, status=status.HTTP_400_BAD_REQUEST)
        key = data.get('key')
        messageID = data.get('messageID')
        
        keyValid, user = keyisValid(key)
        if keyValid:   
            msg = MessageModel.objects.get(Q(user=user, pk=messageID) | Q(recipient=user, pk=messageID))
            serializer = MessageModelSerializer(msg)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:   
            return Response({'error_header':'Something went wrong','error_body': "Something went wrong, please try again later.", "actions": [{"error_code": "1001", 'error_message': 'Try Again'}]}, status=status.HTTP_200_OK)
        
  

@api_view(['POST'])
def sendMessage(request):         
    if request.method == 'POST':
        data = request.data
        if data.get('key') == None or data.get('target') == None or data.get('body') == None:
            return Response({'error': "Invalid body parameter, body must contain 'key', 'body' and 'target'"}, status=status.HTTP_400_BAD_REQUEST)
        key = data.get('key')
        target = data.get('target')
        body = data.get('body')
        keyValid, user = keyisValid(key)
        usernameValid, recipient = usernameisValid(target)
        if keyValid and usernameValid:
            message = MessageModel.objects.create(user=user, recipient=recipient, body=body)
            serializer = MessageModelSerializer(message).data
            return Response(serializer, status=status.HTTP_202_ACCEPTED)
        else:   
            return Response({'error_header':'Something went wrong','error_body': "Something went wrong, please try again later.", "actions": [{"error_code": "1001", 'error_message': 'Try Again'}]}, status=status.HTTP_200_OK)
        


@api_view(["POST"])
def chatUsers(request): 
    if request.method == 'POST':
        data = request.data
        if data.get('key') == None:
            return Response({'error': "Invalid body parameter, body must contain 'key' and optional agument 'limit'"}, status=status.HTTP_400_BAD_REQUEST)
        key = data.get('key')
        
        if data.get('limit') != None:
            limit = int(data.get('limit')) 
        else:
            limit = 15

        keyValid, user = keyisValid(key)
        if keyValid:   
            
            #latest_users = MessageModel.filter(user=user).latest('pk').values('recipient').order_by('pk')
            
            latest_users = list(set(MessageModel.objects.filter(user=user).values_list('recipient', flat=True).order_by('pk')))[:limit]
            allData = []
            
            for chat_user_pk in latest_users:
                data = {}
                i = user_details.objects.get(pk = chat_user_pk)
                data["name"] = i.name
                data["username"] = i.username
                if i.showLastsSeen: 
                    try:
                        last_seen_obj = lastSeen.objects.get(user=i)
                        data["showLastsSeen"] = i.showLastsSeen
                        data["activeNow"] = last_seen_obj.activeNow
                        data["lastSeen"] = last_seen_obj.lastSeen
                    except:
                        data["showLastsSeen"] = False
                else:
                    data["showLastsSeen"] = i.showLastsSeen
  
                try:
                    data["profile_picture"] = i.profile_picture.url 
                except:
                    data["profile_picture"] = None


                unseen_messages_count  = 0
                latest_10_messages = MessageModel.objects.all().filter(Q(recipient=i, user=user) | Q(user=i, recipient=user)).order_by('-pk')[:10:-1]
                for message in latest_10_messages:
                    if message.seen == False:
                        unseen_messages_count = unseen_messages_count + 1 
                
                if unseen_messages_count == 0:

                    liked = likedStream.objects.all().filter(user=user, timestamp__gt=latest_10_messages[-1].timestamp).exists()
                    #print(latest_10_messages[-1].timestamp)
                    #print(liked)
                    if liked:
                        data["unseen_chat"] = True
                        data["preview"] = "Liked a message"
                    else:
                        data["unseen_chat"] = False
                elif unseen_messages_count == 1:
                    data["unseen_chat"] = True
                    data["preview"] = latest_10_messages[-1].body
                elif unseen_messages_count > 9:
                    data["unseen_chat"] = True
                    data["preview"] = "9+ new messages"
                else:
                    data["unseen_chat"] = True
                    data["preview"] = "{} new messages".format(str(unseen_messages_count))


                allData.append(data)
            #print(allData)
            #msg = MessageModel.objects.latest().filter(user=user)
           

            #serializer = MessageModelSerializer(msg, many = True)
            #msg = MessageModel.objects.latest().filter(user=user)
            return Response(allData, status=status.HTTP_202_ACCEPTED)
        else:   
            return Response({'error_header':'Something went wrong','error_body': "Something went wrong, please try again later.", "actions": [{"error_code": "1001", 'error_message': 'Try Again'}]}, status=status.HTTP_200_OK)
        
   


'''
class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(recipient=request.user) |
                                             Q(user=request.user))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=request.user, user__username=target) |
                Q(recipient__username=target, user=request.user))
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=request.user) |
                                 Q(user=request.user))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)
'''