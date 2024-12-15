from .models import User, Tenant, Room, Building
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['password','username','is_Admin']
        extra_kwargs={'password':{'write_only':True}}
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Get the default token
        token = super().get_token(user)
        
        # Add custom claims
        #adding aditional information to the token
        #token['username'] = user.username
        # token['email'] = user.email
        
        return token
    
    def validate(self, attrs):
        # Get the default validation data
        try:
            # Attempt default validation
            data = super().validate(attrs)
        except (InvalidToken, TokenError) as e:
            # Custom error handling
            raise serializers.ValidationError({
                'status': 'error',
                'message': 'Invalid credentials',
                'details': str(e)
            })
        
        # Add additional user information to the response
        user = self.user
        # if not user.is_superuser:
        #        raise serializers.ValidationError({
        #         'status': 'error',
        #         'message': 'Invalid credentials',
        #     })
        data.update({
            'isAdmin':user.is_Admin,
            'username':user.username
        })
        print(data)
        
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  
    
class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Building
        fields='__all__'
        
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'    
class TenantSerializer(serializers.ModelSerializer):
    room_name = serializers.SerializerMethodField(method_name="get_name")

    class Meta:
        model = Tenant
        fields = ['password', 'username', 'is_tenant', 'phone','id', 'room', 'room_name']
        # fields = '__all__'

    def get_name(self, obj):
        # Accessing `room` directly on the instance and then its `room_no` field.
        return obj.room.room_no if obj.room else None

    # def validate_phone(self, value):
    #     # Ensure the phone is a valid string of 10 digits
    #     if not value.isdigit() or len(value) != 10:
    #         raise serializers.ValidationError("Phone number must be a string of exactly 10 digits.")
    #     return value            

    # def validate_room(self, value):
    #     """Ensure the room exists."""
    #     if not Room.objects.filter(pk=value.id if isinstance(value, Room) else value).exists():
    #         raise serializers.ValidationError(f"Room with id '{value}' does not exist.")
    #     return value