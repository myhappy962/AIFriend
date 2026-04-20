from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character, Voice
from web.views.utils.photo import remove_old_photo
import traceback  # 新增：用于打印具体的错误信息


class UpdateCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            character_id = request.data['character_id']
            character = Character.objects.get(id=character_id, author__user=request.user)
            name = request.data['name'].strip()

            # 【修改点 1】使用 .get()，如果前端没传 voice_id，则默认为 None，防止报 KeyError
            voice_id = request.data.get('voice_id')

            profile = request.data['profile'].strip()[:100000]
            photo = request.FILES.get('photo', None)
            background_image = request.FILES.get('background_image', None)

            if not name:
                return Response({
                    'result': "名字不能为空"
                })
            if not profile:
                return Response({
                    'result': '角色介绍不能为空'
                })
            if photo:
                remove_old_photo(character.photo)
                character.photo = photo
            if background_image:
                remove_old_photo(character.background_image)
                character.background_image = background_image

            # 【修改点 2】只有当前端传了 voice_id 时，才去更新声音
            if voice_id:
                voice = Voice.objects.get(id=voice_id)
                character.voice = voice

            character.name = name
            character.profile = profile
            character.update_time = now()
            character.save()
            return Response({
                'result': 'success',
            })

        except Exception as e:
            # 【修改点 3】将具体的错误打印在你的运行终端（控制台）里，方便以后排查报错
            print(f"更新角色失败，错误信息: {e}")
            traceback.print_exc()
            return Response({
                'result': '系统异常，请稍后重试'
            })