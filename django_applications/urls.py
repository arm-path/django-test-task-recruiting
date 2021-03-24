from django.urls import path

from django_applications.views import \
    primary, \
    RecruitCreateView, \
    SithFormView, \
    TestDetailView, \
    SithRecruitListView, \
    SithListView

urlpatterns = [
    path('', primary, name='home_page'),
    path('recruit/', RecruitCreateView.as_view(), name='recruit'),
    path('recruit-<int:recruit_id>/test/<slug:orden_code>/', TestDetailView.as_view(), name='test'),
    path('sith/', SithFormView.as_view(), name='sith'),
    path('siths/', SithListView.as_view(), name='siths'),
    path('sith-<int:sith_id>/', SithRecruitListView.as_view(), name='sith_page'),
    path('sith-<int:sith_id>/planet-<int:planet_id>/', SithRecruitListView.as_view(), name='sith_page_planet'),
    path('sith-<int:sith_id>/recruit-<int:recruit_id>/', SithRecruitListView.as_view(), name='sith_page_recruit'),
    path('sith-<int:sith_id>/my_recruit-<int:my_recruit_id>/', SithRecruitListView.as_view(),
         name='sith_page_my_recruit'),
]
