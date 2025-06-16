from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import UserProfile, CDA, Levy, UserLevy, Payment, ExecutiveMember, Event, CommunityInfo, Defaulter, NavbarImage, PaidMember, Committee, CommitteeMember, CommitteeToDo, CommitteeAchievement

def home(request):
    executive_members = ExecutiveMember.objects.all()
    upcoming_events = Event.objects.all().order_by('date')
    community_info = CommunityInfo.objects.all().order_by('-published_date')
    defaulters = Defaulter.objects.all()
    paid_members = PaidMember.objects.all().order_by('-payment_date')
    left_image = NavbarImage.objects.filter(position='left').first()
    right_image = NavbarImage.objects.filter(position='right').first()
    context = {
        'executive_members': executive_members,
        'upcoming_events': upcoming_events,
        'community_info': community_info,
        'defaulters': defaulters,
        'paid_members': paid_members,
        'left_image': left_image,
        'right_image': right_image
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_levies = UserLevy.objects.filter(user=request.user)
    payments = Payment.objects.filter(user_levy__user=request.user)
    outstanding_levies = UserLevy.objects.filter(user=request.user, is_paid=False)
    return render(request, 'profile.html', {'user_profile': user_profile, 'user_levies': user_levies, 'payments': payments, 'outstanding_levies': outstanding_levies})

def events(request):
    all_events = Event.objects.all().order_by('date')
    return render(request, 'events.html', {'all_events': all_events})

@login_required
def committee_detail(request, committee_id):
    committee = get_object_or_404(Committee, pk=committee_id)
    members = CommitteeMember.objects.filter(committee=committee)
    todos = CommitteeToDo.objects.filter(committee=committee)
    achievements = CommitteeAchievement.objects.filter(committee=committee)
    context = {
        'committee': committee,
        'members': members,
        'todos': todos,
        'achievements': achievements,
    }
    return render(request, 'committee_detail.html', context)

@login_required
def pay_levy(request, levy_id):
    if request.method == 'POST':
        user_levy = UserLevy.objects.get(id=levy_id, user=request.user)
        notes = request.POST.get('notes', '')
        # Simulate payment success
        Payment.objects.create(user_levy=user_levy, amount_paid=user_levy.amount_due, notes=notes)
        user_levy.is_paid = True
        user_levy.save()
    return redirect('profile')
