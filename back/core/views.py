from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils import ProtectableAPIView
from core.models import User, Image
from core.serializers import PrivateUserSerializer, PublicUserSerializer, ImageSerializer
from core.services import UserService
from utils import INVALID_BODY_ERROR, NOT_FOUND_ERROR, ForbiddenActionError
from utils.supabase_client import SupabaseClient


# Create your views here.
class CurrentUserView(ProtectableAPIView):

    @staticmethod
    def get(request: Request):
        user_serializer = PrivateUserSerializer(request.user)
        return Response(user_serializer.data, 200)

    @staticmethod
    def put(request: Request):
        try:
            user = UserService.update_user(request.user, request.data)
            user_serializer = PrivateUserSerializer(user)
            return Response(user_serializer.data, status=200)

        except ValidationError as e:
            return Response({"error": INVALID_BODY_ERROR, "detail": e.detail}, 400)

        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)

        except User.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model='User')}, 404)


class OtherUsersView(ProtectableAPIView):

    @staticmethod
    def get(request: Request, user_id: str = None):
        """
        Fetch all users or a specific user by user_id.
        """
        if user_id is not None:
            return OtherUsersView._get_user(user_id)
        else:
            return OtherUsersView._get_list()

    @staticmethod
    def _get_list() -> Response:
        users = UserService.fetch_all_users()
        user_serializer = PublicUserSerializer(users, many=True)
        return Response(user_serializer.data, 200)

    @staticmethod
    def _get_user(user_id: str) -> Response:
        try:
            user = UserService.fetch_user_by_id(user_id)
            user_serializer = PublicUserSerializer(user)
            return Response(user_serializer.data, 200)
        except User.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model='User')}, 404)


#############################################
class ImageView(APIView):
    @staticmethod
    def post(request):

        try:
            image = request.FILES["image"]
            image_name = image.name

            supabase = SupabaseClient.get()
            file_data = image.read()

            if Image.objects.filter(name=image_name).exists():
                img_obj = Image.objects.get(name=image_name)

            else :
                print("Uploading image to supabase")
                supabase.storage.from_("profile_pictures").upload(image_name, file_data,
                                                                  {"content-type": request.FILES["image"].content_type})
                image_url = supabase.storage.from_("profile_pictures").get_public_url(image_name)
                img_obj = Image.objects.create(name=image_name, url=image_url)
                img_obj.save()

            image_serializer = ImageSerializer(img_obj)
            return Response(image_serializer.data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
