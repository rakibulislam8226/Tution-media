from django.views.generic import UpdateView, DetailView, ListView, CreateView, DeleteView
from django.http import request, HttpResponseRedirect
from django.shortcuts import redirect, render
from . models import Contact, District, Feedback, Post,Comment
from django.contrib import messages
from . forms import ContactForm, CreatePostForm
from django.urls import reverse_lazy
from django.db.models import Q
from .templatetags import tag

# Create your views here.


def search(request):
    query = request.POST.get('search', ' ')
    if query:
        queryset = (Q(title__icontains=query)) | (Q(category__icontains=query)) | (Q(subject__icontains=query)) | (
            Q(class_in__name__icontains=query)) | (Q(salary__icontains=query))
        results = Post.objects.filter(queryset).distinct()
    else:
        results = []
    context = {
        'results': results
    }
    return render(request, 'blog/search.html', context)


def home(request):
    return render(request, 'blog/home.html')

def about_us(request):
    return render(request, 'blog/about_us.html')


def feedback(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        complain = request.POST['complain']
        obj = Feedback(name=name, phone=phone, email=email, complain=complain)
        obj.save()
        messages.success(request, 'Feedback submit successfully.')
        return redirect('/')
    return render(request, 'blog/feedback.html')


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact request submit successfully.')
            return redirect('/')

    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})


# class PostCreateView(CreateView):
#     model = Post
#     form_class = CreatePostForm
#     template_name = 'blog/createpost.html'
#     # success_url = '/'

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         messages.success(self.request, 'Post created successfully.')
#         return super().form_valid(form)

#     def get_success_url(self):
#         id = self.object.id
#         return reverse_lazy('postlist')


def createpost(request):
    if request.method == "POST":
       form = CreatePostForm(request.POST,request.FILES)
       if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            dis=form.cleaned_data['district']
            if not District.objects.filter(name=dis).exists():
                disobj=District(name=dis)
                disobj.save()
            class_in=form.cleaned_data['class_in']
            for i in class_in:
                obj.class_in.add(i)
                obj.save()
            messages.success(request, 'Post create successfully.')
            return redirect('postlist')
    else:
        form=CreatePostForm(district_set=District.objects.all().order_by('name'))
    return render(request, 'blog/createpost.html', {'form': form})


class PostListView(ListView):
    queryset = Post.objects.all()
    template_name = 'blog/postview.html'
    context_object_name = 'post'


# def postlist(request):
#     post = Post.objects.all()
#     return render(request,'blog/postview.html',{'post':post})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/postdetail.html'
    def get_context_data(self,*args, **kwargs):
        self.object.views.add(self.request.user)

        liked=False
        if self.object.likes.filter(id=self.request.user.id).exists():
            liked=True
        context= super().get_context_data(*args,**kwargs)
        post=context.get('object')
        comments = Comment.objects.filter(post=post.id, parent=None)
        replies = Comment.objects.filter(post=post.id).exclude(parent=None)
        DictofReply={}
        for reply in replies:
            if reply.parent.id not in DictofReply.keys():
                DictofReply[reply.parent.id]=[reply]
            else:
                DictofReply[reply.parent.id].append(reply)
        context['liked']= liked
        context['comments'] = comments
        context['DictofReply'] = DictofReply
        return context

from notifications.signals import notify
def likepost(request,id):
    if request.method=="POST":
        post=Post.objects.get(id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            if request.user != post.user:
                notify.send(request.user, recipient=post.user, verb="has liked your post" + f''' <a href="/postdetail/{post.id}/"> Go </a>''')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def notification(request):
  return render(request, 'userprofile/notification.html')


def addcomment(request):
    if request.method=="POST":
        comment=request.POST['comment']
        parentid = request.POST['parentid']
        postid = request.POST['postid']
        post=Post.objects.get(id=postid)
        if parentid:
            parent=Comment.objects.get(id=parentid)
            newcom=Comment(text=comment,user=request.user,post=post,parent=parent)
            newcom.save()
        else:
            newcom = Comment(text=comment, user=request.user,post=post)
            newcom.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deletecomment(request,id):
    comment=Comment.objects.get(id=id)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class PostEditView(UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'blog/createpost.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Post Edited Successfully')
        return super().form_valid(form)

    def get_success_url(self):
        id = self.object.id
        return reverse_lazy('postdetail', kwargs={'pk': id})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/postdelete.html'

    def get_success_url(self):
        id = self.object.id
        messages.success(self.request, 'Deleted successfully')
        return reverse_lazy('postlist')
