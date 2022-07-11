from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # UserProfile.objects.filter(is_active=False).update(user=3)
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()
        comments = Comment.objects.all().order_by('-created_on')

        print("POSTS")
        print(comments)

        post_com_dict = {}

        # print(posts[0].objects)
        for post in posts:
            print("post")
            print(post.pk)
            print(post.author)
            user = UserProfile.objects.filter(user=post.author)
            print("user: ", user.values())
            data = {}
            for key in user.values():
                print(key["is_active"])
                is_active = key["is_active"]

            print("AFTER")
            print(data)
            comments = Comment.objects.filter(post=post.pk).order_by('-created_on')
            comment_users = []
            for comment in comments.values():
                print("comment: ")
                print(comment["author_id"])
                user = UserProfile.objects.filter(user = comment["author_id"])
                print("User values: ", user.values('user_id', 'is_active'))
                comment_users.append(user.values('user_id', 'is_active'))


            if len(comments) > 3:
                post_com_dict[post] = comments[0:3]
            else:
                post_com_dict[post] = comments

        print("POSTS")
        print(post_com_dict)

        print(comment_users)

        context = {
            'post_list': post_com_dict,
            'form': form,
            'is_active': is_active,
            'comment_users' : comment_users

        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        print("POSTS")
        print(posts)
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form
            # 'comments': comments,

        }

        return render(request, 'social/post_list.html', context)

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):

        print("PK: ", pk)
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['is_active']
    template_name = 'social/account_delete.html'

    def get_success_url(self):
        print("Account kwargs: ")
        print(self.kwargs)
        pk = self.kwargs['pk']
        self.is_active = False
        return reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        print("self.kwargs : ", self.kwargs)
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self, *args, **kwargs):
        post = self.get_object()
        print("args")
        print(self.args)

        print("kwargs")
        print(self.kwargs)

        post1 = Post.objects.get(pk=self.kwargs['post_pk'])
        print("post1")
        print(post1)

        print("delete comment post var: ", post)
        return self.request.user == post.author or post1.author == self.request.user

class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        context = {
            'user': user,
            'profile': profile,
            'posts': posts
        }

        return render(request, 'social/profile.html', context)

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
