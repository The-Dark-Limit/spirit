# from core.domain.entities import User
# from core.domain.value_objects import Email, Password
# from core.interfaces.abstractions.user_repository import IUserRepository
#
#
# class RegisterUserUseCase:
#     def __init__(self, user_repository: IUserRepository):
#         self.user_repository = user_repository
#
#     async def execute(self, email: str, password: str) -> User:
#         email_value_object = Email(email)
#         password_value_object = Password(password)
#
#         if not email_value_object.is_valid():
#             raise ValueError('Invalid email address.')
#
#         if not password_value_object.is_valid():
#             raise ValueError('Password must be at least 8 characters long.')
#
#         existing_user = await self.user_repository.find_by_email(email_value_object.value)
#         if existing_user is not None:
#             raise ValueError('Email already exists.')
#
#         new_user = User(
#             id=None,
#             email=email_value_object.value,
#             password=password_value_object.hashed_value
#         )
#
#         created_user = await self.user_repository.create(new_user)
#         return created_user
#
#
#
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from core.domain.use_cases.register_user_use_case import RegisterUserUseCase
# from core.interfaces.implementations.django_user_repository import DjangoUserRepository
#
#
# class RegisterView(APIView):
#     def post(self, request):
#         register_user_use_case = RegisterUserUseCase(DjangoUserRepository())
#         try:
#             user = register_user_use_case.execute(request.data['email'], request.data['password'])
#             return Response({'message': 'User registered successfully.'}, status=201)
#         except ValueError as e:
#             return Response({'error': str(e)}, status=400)
