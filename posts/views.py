# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from posts.models import Post, Comment
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from posts.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
	posts = Post.objects.filter(status__exact='PUBLISHED').order_by('-pub_date')
	paginator = Paginator(posts, 10)
	recent = posts[:3]
	page = request.GET.get('page')
	try:
		this_posts = paginator.page(page)
	except PageNotAnInteger:
		this_posts = paginator.page(1)
	except EmptyPage:
		this_posts = paginator.page(paginator.num_pages)

	context_var = RequestContext(request, {'posts' : this_posts, 'recent':recent})
	return render_to_response('index.html', context_var)

def view_post(request, slug=None):
	try:
		post = Post.objects.get(slug=slug)
	except ObjectDoesNotExist:
		raise Http404
	if request.method == 'POST':
		comment = Comment(post=post)
		comment_form = CommentForm(request.POST, instance=comment)
		if comment_form.is_valid():
			comment_form.save()
			comment_form1 = CommentForm()
			comments = post.comment_set.filter(status__exact='A')
			context = RequestContext(request, { 'post' : post, 
				'comment_form' : comment_form1, 
				'comments' : comments,
				'len_comments' : len(comments)})
			return render_to_response('post.html', context)
		else:
			return HttpResponseRedirect(post.get_absolute_url())
	else:
		comments = post.comment_set.filter(status__exact='A')
		comment = CommentForm()
		context = RequestContext(request, { 'post' : post, 
			'comment_form': comment, 
			'comments':comments,
			'len_comments' : len(comments)})
		return render_to_response('post.html', context)
	return HttpResponse('/')