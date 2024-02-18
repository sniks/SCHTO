from django.core.mail import send_mail
from django.http import HttpResponseServerError, HttpResponse
from .models import Blog, Board, Sponsor, Testimonial, Payment

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils import timezone
import os
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.core.files.storage import default_storage
from .forms import NewsletterSubscriptionForm
from django.contrib.auth.decorators import login_required

def index(request):
    boards = Board.objects.order_by('-value')[:8]
    blogs = Blog.objects.filter(published=1).order_by('-id')[:2]
    testimonials = Testimonial.objects.all()[:10]
    sponsors = Sponsor.objects.all()[:10]

    return render(request, 'welcome.html', {'boards': boards, 'blogs': blogs, 'testimonials': testimonials, 'sponsors': sponsors})

def sendmail(request):
    if request.method == 'POST':
        data = request.POST
        body = ', '.join([f"{k}='{v}'" for k, v in data.items()])

        # Send email
        subject = 'Feedback Form Submission'
        sender_email = 'info@secondchildhoodtrust.org'
        recipient_email = 'info@secondchildhoodtrust.org'
        message = f"{body}\n"
        try:
            send_mail(subject, message, sender_email, [recipient_email])
            return HttpResponse('success')
        except Exception as e:
            print(e)
            return HttpResponseServerError('failed')

def about(request):
    boards = Board.objects.filter(designation='volunteer').order_by('-value')
    return render(request, 'about.html', {'boards': boards})

def contact(request):
    return render(request, 'contact.html')

def privacy(request):
    return render(request, 'privacy.html')

def tc(request):
    return render(request, 't&c.html')

def rc(request):
    return render(request, 'r&c.html')

def blog_index(request):
    # Get all blogs
    all_blogs = Blog.objects.all()

    # Number of blogs per page
    per_page = 2

    # Create a paginator object
    paginator = Paginator(all_blogs, per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page', 1)

    try:
        # Get the blogs for the requested page
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page.
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'blog.html', {'blogs': blogs})

def blog_single(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.views = int(blog.views) + 1 if blog.views else 1
    blog.save()
    blog.tag_list = blog.tags.split(',')
    blogs = Blog.objects.all()
    sliced_blogs = blogs.order_by('?')[:3]
    return render(request, 'blogdetails.html', {'blog': blog, 'blogs': sliced_blogs})

def show_blog_list(request):
    if request.user.is_authenticated:
        blog_list = Blog.objects.all()
        paginator = Paginator(blog_list, 10)  # Show 10 blogs per page

        page = request.GET.get('page')
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        return render(request, 'admin/pages/list-blogs-admin.html', {'blogs': blogs})
    else:
        messages.warning(request, 'You have to log in first')
        return redirect('login')

def blog_show_create(request, id=None):
    if not request.user.is_authenticated:
        messages.warning(request, 'You have to log in first')
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        tags = request.POST.get('tags')
        image = request.FILES.get('image')

        # Process image

        # Use MEDIA_ROOT for file storage
        if 'image' in request.FILES:
            imagename = f'{timezone.now().timestamp()}_{image.name}'
            uploaded_file = request.FILES['image']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT+ '/blog')
            image_path = fs.save(imagename, uploaded_file)

        # Create or update blog entry
        if id:
            # If id is present, update an existing blog
            blog = get_object_or_404(Blog, id=id)
            blog.title = title
            blog.description = description
            blog.tags = tags
            blog.updated_at  = timezone.now()
            if image:
                blog.image = image_path
            blog.save()
            messages.success(request, 'Blog has been updated.')
        else:
            # If id is not present, create a new blog
            blog = Blog(title=title, description=description, tags=tags, image=image_path,created_at=timezone.now())
            blog.save()
            messages.success(request, 'New blog has been created.')

        return redirect('blogs_create')

    # If it's not a POST request, handle GET request
    return render(request, 'admin/pages/create-blog.html', {'id': id})



def blog_show_edit(request, id):
    if request.user.is_authenticated:
        row = get_object_or_404(Blog, id=id)
        return render(request, 'admin/pages/create-blog.html', {'row': row})
    else:
        messages.warning(request, 'You have to log in first')
        return redirect('login')

def blog_activate_deactivate(request, id):
    if request.user.is_authenticated:
        blog = get_object_or_404(Blog, id=id)
        if blog.published:
            blog.published = False
        else:
            blog.published = True
        blog.save()
        messages.success(request, f'Status of post (ID-{blog.id}) has been changed.')
        return redirect('blogs')
    else:
        messages.warning(request, 'You have to log in first')
        return redirect('login')
    
def blog_delete(request, id):
    if request.user.is_authenticated:
        blog = get_object_or_404(Blog, id=id)
        blog.delete()
        messages.success(request, f'Post (ID-{blog.id}) has been Deleted.')
        return redirect('blogs')
    else:
        messages.warning(request, 'You have to log in first')
        return redirect('login')

def board_show(request):
    boards = Board.objects.order_by('-value').paginate(page=request.GET.get('page', 1), per_page=10)
    return render(request, 'front/pages/board-members.html', {'boards': boards})

def board_show_filter(request, skey):
    boards = Board.objects.filter(fullname__istartswith=skey).paginate(page=request.GET.get('page', 1), per_page=10)
    return render(request, 'front/pages/board-members.html', {'boards': boards})

def show_board_list(request):
    if request.user.is_authenticated:
        boards = Board.objects.order_by('value').all()
        return render(request, 'admin/pages/list-board-admin.html', {'boards': boards})
    else:
        messages.warning(request, 'You have to log in first')
        return redirect('login')

def board_show_create(request, id=None):
    if not request.user.is_authenticated:
        messages.warning(request, 'You have to log in first')
        return redirect('login')

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        designation = request.POST.get('designation')
        value = request.POST.get('value')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')

        # Process image
        imagename = 'default.png'

        # Use MEDIA_ROOT for file storage
        if 'image' in request.FILES:
            imagename = f'{timezone.now().timestamp()}_{image.name}'
            uploaded_file = request.FILES['image']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/board')
            image_path = fs.save(imagename, uploaded_file)

        # Create or update board entry
        if id:
            # If id is present, update an existing board
            board = get_object_or_404(Board, id=id)
            board.fullname = fullname
            board.designation = designation
            board.value = value
            board.address = address
            board.gender = gender
            board.phone = phone
            if 'image' in request.FILES:
                board.image = image_path
            board.save()
            messages.success(request, 'Board member record has been updated.')
        else:
            # If id is not present, create a new board member
            board = Board(fullname=fullname, designation=designation, value=value, address=address,
                          gender=gender, phone=phone, image=image_path)
            board.save()
            messages.success(request, 'New board member record has been added.')

        return redirect('boards')

    # If it's not a POST request, handle GET request
    return render(request, 'admin/pages/create-board.html', {'id': id})


def board_show_edit(request, id):
    if request.user.is_authenticated:
        row = get_object_or_404(Board, id=id)
        return render(request, 'admin/pages/create-board.html', {'row': row})
    else:
        messages.warning(request, 'You have to log in first')
        return redirect('login')
    
def board_delete(request, id):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, id=id)
        board.delete()
        messages.success(request, f'Post (ID-{board.id}) has been Deleted.')
        return redirect('boards')
    else:
        messages.warning(request, 'You have to log in first')
        return redirect('login')

@csrf_exempt
def payment_store(request):
    if request.method == 'POST':
        # Parse JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))

        # Validate the request data
        name = data.get('name')
        amount = data.get('amount')
        razorpay_payment_id = data.get('razorpay_payment_id')

        if name and amount and razorpay_payment_id:
            # Store the payment data in the Payment model
            payment = Payment.objects.create(
                name=name,
                amount=amount,
                razorpay_payment_id=razorpay_payment_id,
                # Set additional fields as needed
            )

            # Return a JSON response
            return JsonResponse({'success': 'Success'})
        else:
            return JsonResponse({'success': 'failed', 'error': 'Invalid data'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a success page

def show_sponsor_list(request):
    if request.user.is_authenticated:
        sponsors = Sponsor.objects.all()
        return render(request, 'admin/pages/list-sponsors-admin.html', {'sponsors': sponsors})
    else:
        return redirect('login')

def sponsor_show_create(request, id=None):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        try:
            if 'image' in request.FILES:
                image = request.FILES['image']
                imagename = f'{timezone.now().timestamp()}_{image.name}'
                file_path = default_storage.save(f'sponsor/'+imagename, image)

            if id:
                # If id is present, update an existing sponsor
                sponsor = get_object_or_404(Sponsor, id=id)
                if 'image' in request.FILES:
                    sponsor.image = imagename

                sponsor.save()
                messages.success(request, 'Sponsor has been updated.')
            else:
                # If id is not present, create a new sponsor
                Sponsor.objects.create(image=file_path if 'image' in request.FILES else None)
                messages.success(request, 'New sponsor has been created.')

            return redirect('sponsors')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('sponsors')

    return render(request, 'admin/pages/create-sponsors.html', {'id': id})

def sponsor_show_edit(request, id):
    if request.user.is_authenticated:
        return render(request, 'admin/pages/create-sponsors.html', {'row': id})
    else:
        return redirect('login')

def sponsors_delete(request, id):
    if request.user.is_authenticated:
        sponsor = get_object_or_404(Sponsor, id=id)
        sponsor.delete()
        messages.success(request, f'Post (ID-{sponsor.id}) has been Deleted.')
        return redirect('sponsors')
    else:
        messages.warning(request, 'You have to log in first')
        return redirect('login')
            
def show_testimonial_list(request):
    if request.user.is_authenticated:
        testimonials = Testimonial.objects.all()

        # Number of testimonials to display per page
        items_per_page = 10
        paginator = Paginator(testimonials, items_per_page)

        # Get the current page number from the request's GET parameters
        page = request.GET.get('page')

        try:
            # Get the testimonial objects for the current page
            testimonials_page = paginator.page(page)
        except PageNotAnInteger:
            # If the page parameter is not an integer, show the first page
            testimonials_page = paginator.page(1)
        except EmptyPage:
            # If the page is out of range, show the last page
            testimonials_page = paginator.page(paginator.num_pages)

        return render(request, 'admin/pages/list-testimonial-admin.html', {'testimonials': testimonials_page})
    else:
        return redirect('login')

def testimonial_show_create(request, id=None):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        try:
            if 'image' in request.FILES:
                image = request.FILES['image']
                imagename = f'{timezone.now().timestamp()}_{image.name}'
                default_storage.save(f'testimonial/'+imagename, image)

            if id:
                # If id is present, update an existing testimonial
                testimonial = get_object_or_404(Testimonial, id=id)
                testimonial.fullname = request.POST['fullname']
                testimonial.designation = request.POST['designation']
                testimonial.organization = request.POST.get('organization', '')
                testimonial.description = request.POST['description']

                if 'image' in request.FILES:
                    testimonial.image = imagename

                testimonial.save()
                messages.success(request, 'Testimonial has been updated.')
            else:
                # If id is not present, create a new testimonial
                Testimonial.objects.create(
                    fullname=request.POST['fullname'],
                    designation=request.POST['designation'],
                    organization=request.POST.get('organization', ''),
                    description=request.POST['description'],
                    image=imagename if 'image' in request.FILES else None
                )
                messages.success(request, 'New testimonial has been created.')

            return redirect('testimonials')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('testimonials')

    return render(request, 'admin/pages/create-testimonials.html', {'id': id})

def testimonial_show_edit(request, id):
    if request.user.is_authenticated:
        testimonial = Testimonial.objects.get(id=id)    
        return render(request, 'admin/pages/create-testimonials.html', {'row': testimonial})
    else:
        return redirect('login')

def testimonial_delete(request, id):
    if request.user.is_authenticated:
        testimonial = get_object_or_404(Testimonial, id=id)
        testimonial.delete()
        messages.success(request, f'Post (ID-{testimonial.id}) has been Deleted.')
        return redirect('testimonials')
    else:
        messages.warning(request, 'You have to log in first')
        return redirect('login')
