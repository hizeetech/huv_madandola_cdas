from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import AdvertItemForm, AdvertImageFormSet, DonationProofForm
from .models import ProjectDonation

from .models import (
    CDA, UserProfile, Levy, UserLevy, Payment, ExecutiveMember, Defaulter, 
    Event, CommunityInfo, NavbarImage, PaidMember, Committee, CommitteeMember, 
    CommitteeToDo, CommitteeAchievement, AdvertCategory, AdvertItem, AdvertImage, 
    Artisan, Professional, ProjectDonation, ProjectImage, DonationProof, Proposal
)
from .forms import AdvertItemForm, AdvertImageFormSet, DonationProofForm
from django.contrib import messages


def home(request):
    executive_members = ExecutiveMember.objects.all()
    committees = Committee.objects.all()
    upcoming_events = Event.objects.all().order_by('date')
    community_info = CommunityInfo.objects.all().order_by('-published_date')
    defaulters = Defaulter.objects.all()

    selected_cda = request.GET.get('cda', '').strip()
    selected_debt_for = request.GET.get('debt_for', '').strip()

    if selected_cda:
        defaulters = defaulters.filter(cda__iexact=selected_cda)

    if selected_debt_for:
        defaulters = defaulters.filter(title_defaulted__iexact=selected_debt_for)

    paid_members = PaidMember.objects.all().order_by('-payment_date')
    left_image = NavbarImage.objects.filter(position='left').first()
    right_image = NavbarImage.objects.filter(position='right').first()
    project_donations = ProjectDonation.objects.all()

    context = {
        'executive_members': executive_members,
        'committees': committees,
        'upcoming_events': upcoming_events,
        'community_info': community_info,
        'defaulters': defaulters,
        'paid_members': paid_members,
        'left_image': left_image,
        'right_image': right_image,
        'cdas': Defaulter.cda_choices,
        'debt_for_choices': Defaulter.debt_for_choices,
        'selected_cda': selected_cda,
        'selected_debt_for': selected_debt_for,
        'project_donations': ProjectDonation.objects.all().prefetch_related('images'),
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate user until approved
            user.save()
            UserProfile.objects.create(user=user, is_approved=False)
            return render(request, 'registration_pending.html') # Redirect to a pending approval page
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
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_levies = UserLevy.objects.filter(user=request.user)
    payments = Payment.objects.filter(user_levy__user=request.user)
    outstanding_levies = UserLevy.objects.filter(user=request.user, is_paid=False)
    return render(request, 'profile.html', {'user_profile': user_profile, 'user_levies': user_levies, 'payments': payments, 'outstanding_levies': outstanding_levies})

def events(request):
    all_events = Event.objects.all().order_by('date')
    return render(request, 'events.html', {'all_events': all_events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_detail.html', {'event': event})

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


def advert_list(request):
    category_name = request.GET.get('category')
    user_filter = request.GET.get('user')
    
    if category_name:
        advert_items = AdvertItem.objects.filter(is_approved=True, category=category_name).order_by('-published_date')
    elif user_filter and request.user.is_authenticated:
        advert_items = AdvertItem.objects.filter(is_approved=True, user=request.user).order_by('-published_date')
    else:
        advert_items = AdvertItem.objects.filter(is_approved=True).order_by('-published_date')

    context = {
        'advert_items': advert_items
    }
    return render(request, 'advert_list.html', context)

def advert_detail(request, pk):
    advert_item = get_object_or_404(AdvertItem, pk=pk)
    return render(request, 'advert_detail.html', {'advert_item': advert_item})

def submit_proposal(request, advert_id):
    if request.method == 'POST':
        advert = get_object_or_404(AdvertItem, pk=advert_id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        proposed_amount = request.POST.get('proposed_amount')
        notes = request.POST.get('notes', '')
        
        Proposal.objects.create(
            advert=advert,
            name=name,
            email=email,
            phone_number=phone_number,
            proposed_amount=proposed_amount,
            notes=notes
        )
        
        messages.success(request, 'Your Negotiated Proposal is submitted successfully. Kindly wait patiently while the advertiser will communicate with you. Thank you')
        return redirect('advert_detail', pk=advert_id)
    return redirect('home')

@login_required
def proposal_list(request):
    proposals = Proposal.objects.filter(advert__user=request.user).order_by('-created_at')
    return render(request, 'proposal_list.html', {'proposals': proposals})


@login_required
def create_advert(request):
    if request.method == 'POST':
        form = AdvertItemForm(request.POST, request.FILES)
        formset = AdvertImageFormSet(request.POST, request.FILES, queryset=AdvertImage.objects.none())
        print(f"Debug: Form is valid: {form.is_valid()}")
        print(f"Debug: Form errors: {form.errors}")
        print(f"Debug: Formset is valid: {formset.is_valid()}")
        print(f"Debug: Formset errors: {formset.errors}")
        if form.is_valid() and formset.is_valid():
            advert_item = form.save(commit=False)
            advert_item.user = request.user
            advert_item.is_approved = False  # Set to False for admin approval
            advert_item.save()
            print(f"Debug: Formset cleaned data: {formset.cleaned_data}")
            for image_data in formset.cleaned_data:
                # Check if the formset data is not empty and not marked for deletion
                if image_data and not image_data.get('DELETE', False):
                    image = image_data.get('image')
                    is_main = image_data.get('is_main', False)
                    if image:
                        AdvertImage.objects.create(advert_item=advert_item, image=image, is_main=is_main)
            return redirect('advert_detail', pk=advert_item.pk)
    else:
        form = AdvertItemForm()
        formset = AdvertImageFormSet(queryset=AdvertImage.objects.none())
    return render(request, 'create_advert.html', {'form': form, 'formset': formset})

@login_required
def artisans_list(request):
    artisans = Artisan.objects.all()
    return render(request, 'artisans_list.html', {'artisans': artisans})

@login_required
def professionals_list(request):
    professionals = Professional.objects.all()
    return render(request, 'professionals_list.html', {'professionals': professionals})

@login_required
def project_donations_list(request):
    project_donations = ProjectDonation.objects.all()
    return render(request, 'project_donations_list.html', {'project_donations': project_donations})

def past_executives(request):
    past_members = ExecutiveMember.objects.filter(end_date__lt=timezone.now()).order_by('-start_date')
    context = {
        'executive_members': past_members,
        'title': 'Past Executive Members'
    }
    return render(request, 'executive_members.html', context)

def present_executives(request):
    present_members = ExecutiveMember.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).order_by('start_date')
    context = {
        'executive_members': present_members,
        'title': 'Present Executive Members'
    }
    return render(request, 'executive_members.html', context)

@login_required
def upload_donation_proof(request, donation_id):
    project_donation = get_object_or_404(ProjectDonation, pk=donation_id)
    if request.method == 'POST':
        form = DonationProofForm(request.POST, request.FILES)
        if form.is_valid():
            donation_proof = form.save(commit=False)
            donation_proof.project_donation = project_donation
            donation_proof.save()
            return redirect('project_donations_list')  # Redirect to the donations list after successful upload
    else:
        form = DonationProofForm(initial={'donation_reference_number': project_donation.reference_number})
    return render(request, 'upload_donation_proof.html', {'form': form, 'project_donation': project_donation})
