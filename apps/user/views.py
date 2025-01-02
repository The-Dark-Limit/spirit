from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.dependencies.di_config import configure_di
from core.domain.use_cases.register_user_use_case import RegisterUserUseCase

class RegisterUserView(APIView):
    def post(self, request):
        container = configure_di()
        user_service = container.resolve(UserService)
        register_user_use_case = RegisterUserUseCase(user_service)

        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = register_user_use_case.execute(email, password)
            return Response({'message': f'Пользователь {user.email.value} успешно зарегистрирован.'}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
