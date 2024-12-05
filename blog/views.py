from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm # type: ignore

# Afficher tous les articles
def post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

# Afficher un article en détail et ses commentaires
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all()  # Récupérer les commentaires liés à cet article
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Associer le commentaire à l'article
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

# Créer un nouvel article
def post_create(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_form.html', {'form': form})

# Modifier un article existant
def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

# Supprimer un article
def post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})