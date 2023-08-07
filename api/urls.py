from django.urls import path
from .views import (
    BookListCreateView, UserListCreateView, BorrowBook, ReturnBook, DeleteUser,BookDetailUpdateView
    ,SignUp, SignIn,MemberDetailUpdateView
)

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('books/<int:book_id>/', BookDetailUpdateView.as_view(), name='book-detail-update'),
    path('borrow/<int:book_id>/', BorrowBook.as_view(), name='borrow-book'),
    path('return/<int:book_id>/', ReturnBook.as_view(), name='return-book'),
    path('delete-user/<int:member_id>/', DeleteUser.as_view(), name='delete-user'),
    path('update-member/<int:member_id>/', MemberDetailUpdateView.as_view(), name='update_member'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
]
