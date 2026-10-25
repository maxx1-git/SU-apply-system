from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount

from .models import Application


@login_required
def apply(request):
    # Get the Discord account linked to the currently authenticated user.
    social_account = SocialAccount.objects.filter(
        user=request.user,
        provider="discord",
    ).first()

    if social_account is None:
        messages.error(request, "اربط حساب Discord الخاص بك أولاً ثم حاول مرة أخرى.")
        return redirect("account_login")

    # Never trust a Discord ID submitted by the browser.
    discord_id = social_account.uid

    if request.method == "POST":
        character_name = request.POST.get("character_name", "").strip()
        rank_id = request.POST.get("rank_id", "").strip()
        chase_handling = request.POST.get("chase_handling", "").strip()
        vehicle_experience = request.POST.get("vehicle_experience", "").strip()
        apply_reasons = request.POST.get("apply_reasons", "").strip()
        unit_tasks = request.POST.get("unit_tasks", "").strip()
        vehicle_deploy = request.POST.get("vehicle_deploy", "").strip()
        chase_scenario = request.POST.get("chase_scenario", "").strip()

        if Application.objects.filter(discord_id=discord_id).exists():
            messages.error(request, "هذا الحساب أرسل تقديمًا بالفعل.")
            return redirect("apply")

        try:
            Application.objects.create(
                user=request.user,
                character_name=character_name,
                discord_id=discord_id,
                rank_id=rank_id,
                chase_handling=chase_handling,
                vehicle_experience=vehicle_experience,
                apply_reasons=apply_reasons,
                unit_tasks=unit_tasks,
                vehicle_deploy=vehicle_deploy,
                chase_scenario=chase_scenario,
            )
            messages.success(request, "تم إرسال التقديم بنجاح | انتظر إعلان النتيجة")
            return redirect("index")
        except IntegrityError:
            messages.error(request, "حصل خطأ أثناء إرسال التقديم، حاول مرة أخرى.")
            return redirect("apply")

    return render(
        request,
        "apply/apply.html",
        {"discord_username": social_account.extra_data.get("username", "")},
    )
