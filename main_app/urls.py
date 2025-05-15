from django.urls import path
from .views import (
    CreateUserView,
    LoginView,
    VerifyUserView,
    PetList,
    PetDetail,
    ShelterList,
    ShelterDetail,
    InquiryListCreate,
    InquiryDetail,
    UserAdoptionsAndInquiries
)

urlpatterns = [
    path("auth/sign-up/", CreateUserView.as_view(), name="sign-up"),
    path("auth/sign-in/", LoginView.as_view(), name="sign-in"),
    path("auth/verify/", VerifyUserView.as_view(), name="verify-user"),
    path("pets/", PetList.as_view(), name="pet-list"),
    path("pets/<int:id>/", PetDetail.as_view(), name="pet-detail"),
    path(
        "pets/<int:pet_id>/inquiries/",
        InquiryListCreate.as_view(),
        name="inquiry-list-create",
    ),
    path(
        "pets/<int:pet_id>/inquiries/<int:id>/",
        InquiryDetail.as_view(),
        name="inquiry-detail",
    ),
    path("shelters/", ShelterList.as_view(), name="shelter-list"),
    path("shelters/<int:id>/", ShelterDetail.as_view(), name="shelter-detail"),
    path("user/adoptions/", UserAdoptionsAndInquiries.as_view(), name="user-adoptions"),
]
