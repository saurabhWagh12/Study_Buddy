from rest_framework.response import Response
from rest_framework.decorators import api_view,APIView
from serializer import *
from django.contrib.auth import authenticate
import jwt
import datetime
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


class CustomError(Exception):
    def __init__(self, message="Custom error occurred."):
        self.message = message
        super().__init__(self.message)

@api_view(['POST'])
def makeRequest(request):
    try:
        data = request.data
        
        serializer = EmailSerializer(data={'email': data['fromUser']})
        if serializer.is_valid():
            fromUser = serializer.data['email']
        serializer = EmailSerializer(data={'email': data['toUser']})
        if serializer.is_valid():
            toUser = serializer.data['email']
        
        check = False
        try:
            buddy = Buddy.objects.get(user1=fromUser,user2=toUser)
        except Buddy.DoesNotExist:
            try:
                buddy = Buddy.objects.get(user1=toUser,user2=fromUser)  
            except Buddy.DoesNotExist:
                buddy = None
        
        try:
            Req = Request.objects.get(fromUser=fromUser,toUser=toUser)
        except Request.DoesNotExist:
            try:
                Req = Request.objects.get(fromUser=toUser,toUser=fromUser)  
            except Request.DoesNotExist:
                Req = None
        
        if buddy==None and Req==None:
            check=True
        #Check email existance:
        emailCheck = False
        try:
            userFrom = User.objects.get(email=fromUser)
        except User.DoesNotExist:
            userFrom = None
        try:
            userTo = User.objects.get(email=toUser)
        except User.DoesNotExist:
            userTo = None

        if userTo!=None and userFrom!=None:
            emailCheck = True

        if not emailCheck:
            return Response({'status':400,'message':'Any one or both email does not exists'})

        if check and emailCheck:
            req = Request.objects.create(fromUser=fromUser,toUser=toUser)
            req.save() 
            return Response({'status':200,'message':'Request sent successfully'})
        else:
            return Response({'status':400,'message':'Error already buddies'})
    except Exception as e:
        return Response({'status':400,'message':str(e)})

@api_view(['POST'])
def getAllRequests(request):
    try:
        
        req = Request.objects.filter(toUser=request.data['email'])
        li = []
        for user in req:
            li.append([user.id,user.fromUser])
        return Response({'status':200,'requests':li})
    except Exception as e:
        return Response({'status':400,'message':str(e)})

@api_view(['GET'])
def acceptRequest(request,id):
    try:
        req = Request.objects.get(pk=id)
        try:
            buddy = Buddy.objects.get(user1=req.fromUser,user2=req.toUser)
        except Buddy.DoesNotExist:
            try:
                buddy = Buddy.objects.get(user1=req.toUser,user2=req.fromUser)  
            except Buddy.DoesNotExist:
                buddy = None

        if buddy!=None:
            return Response({'status':400,'message':'Error in Buddy Request handling'})
        else:
            buddy = Buddy.objects.create(user1=req.fromUser,user2=req.toUser)
            buddy.save()
            req.delete()
            return Response({'status':200,'message':'Request accepted successfully'})


    except Exception as e:
        return Response({'status':400,'message':str(e)})


@api_view(['POST'])
def getBuddies(request):
    try:
        user = request.data['user']
        serializer = EmailSerializer(data={"email":user})
        if serializer.is_valid():
            user = serializer.data['email']
        l1 = Buddy.objects.filter(user1=user)
        l2 = Buddy.objects.filter(user2=user)
        l = []
        for buddy in l1:
            l.append(buddy.user2)
        for buddy in l2:
            l.append(buddy.user1)
        
        return Response({'status':200,'buddies':set(l)})
    except Exception as e:
        return Response({'status':400,'message':str(e)})
    

@api_view(['GET','DELETE'])
def deleteRequest(request,id):
    try:
        req = Request.objects.get(pk=id)
        req.delete()
        return Response({'status':200,'message':'Request deleted successfully'})

    except Exception as e:
        return Response({'status':400,'message':str(e)})

@api_view(['POST'])
def removeBuddy(request):
    try:
        email1 = EmailSerializer(data={'email':request.data['email1']})
        if not email1.is_valid():
            raise CustomError("Error in Handling Email-1")
        
        email2 = EmailSerializer(data={'email':request.data['email2']})
        if not email2.is_valid():
            raise CustomError("Error in Handling Email-2")
        
        try:
            buddy = Buddy.objects.get(user1=email1.data['email'],user2=email2.data['email'])
            buddy.delete()
        except Buddy.DoesNotExist:
            try:
                buddy = Buddy.objects.get(user1=email2.data['email'],user2=email1.data['email'])
                buddy.delete()
            except Buddy.DoesNotExist:
                return Response({'status':400,'message':'Invalid Buddy Removal Request'})

        return Response({'status':200,'message':'Successfully removed buddy'})
    except Exception as e:
        return Response({'status':400,'message':str(e)})


@api_view(['POST'])
def deleteUser(request):
    try:
        username = request.data['username']
        user = User.objects.get(username=username)
        buddy1 = Buddy.objects.filter(user1=user.email)
        buddy2 = Buddy.objects.filter(user2=user.email)
        userInfo = UserInfo.objects.get(user=user)
        for buddy in buddy1:
            buddy.delete()
        for buddy in buddy2:
            buddy.delete()
        req = Request.objects.filter(fromUser=user.email)
        for r in req:
            r.delete()
        req = Request.objects.filter(toUser=user.email)
        for r in req:
            r.delete()
        userInfo.delete()
        user.delete()
        return Response({'status':200,'message':'User deleted successfully'})
    except Exception as e:
        return Response({'status':400,'message':str(e)})

class RegisterAPI(APIView):
    def checkEmail(self,email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return True
        return False
    
    def post(self,request):
        try:
            serializer = RegisterSerializer(data={'username':request.data['username'],'email':request.data['email'],'password':request.data['password'],'phone':request.data['phone']})
            if serializer.is_valid():
                check = self.checkEmail(serializer.data['email'])
                if not check:
                    return Response({'status':400,'message':'Email already exists'})
                data = serializer.data
                user = User.objects.create_user(username=data['username'],email=data['email'],password=data['password']) 
                user.save()
                userInfo = UserInfo.objects.create(user=user,phone=data['phone'])
                userInfo.save()
            else:
                return Response({'status':400,'message':'Error in User creation'})

            return Response({'status':200,'message':'User registered successfully'})
            
        except Exception as e:
            return Response({'status':400,'message':str(e)})
        
class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')
            
            credentials = UserSerializer(data={'username':username,'password':password})
            
            if not credentials.is_valid():
                print(credentials.data)
                return Response({'status': 400, 'message': 'Invalid Credentials'})
            
            user = authenticate(username=credentials.data['username'], password=credentials.data['password'])

            if user is not None:

                # Create a JWT token
                now = datetime.now(timezone.utc)

                # Use relativedelta for 1440 minutes
                expiration_time = now + relativedelta(minutes=1440)

                # Use expiration_time in your payload
                payload = {
                    'id': user.id,
                    'exp': expiration_time,
                    'iat': now
                }

                token = jwt.encode(payload, 'secret', algorithm='HS256')
                response = Response({'status': 200, 'token': token})

                # Set the token as a cookie in the response
                # response.set_cookie(key='token', value=token)
                return response
            else:
                return Response({'status': 400, 'message': 'Invalid Credentials'})

        except Exception as e:
            return Response({'status': 400, 'message': 'Error: ' + str(e)})

@api_view(['POST'])
def userDetails(request):
    try:
        token = request.data['token']
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserInfoSerializer(user)  
        return Response({'status': 200, 'data': serializer.data})  

    except Exception as e:
        return Response({'status': 400, 'message': 'Error: ' + str(e)})



