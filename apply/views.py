from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Application


def apply(request):
    if request.method == "POST":
        character_name = request.POST.get("character_name")
        discord_id = request.POST.get("discord_id")
        rank_id = request.POST.get("rank_id")
        chase_handling = request.POST.get("chase_handling")
        vehicle_experience = request.POST.get("vehicle_experience")
        apply_reasons = request.POST.get("apply_reasons")
        unit_tasks = request.POST.get("unit_tasks")
        vehicle_deploy = request.POST.get("vehicle_deploy")
        chase_scenario = request.POST.get("chase_scenario")

     
        if Application.objects.filter(discord_id=discord_id).exists():
            messages.error(request, " معرف ديسكورد مستخدم بالفعل !")
            return redirect("apply")

        try:
            Application.objects.create(
                character_name=character_name,
                discord_id=discord_id,
                rank_id=rank_id,
                chase_handling=chase_handling,
                vehicle_experience=vehicle_experience,
                apply_reasons=apply_reasons,
                unit_tasks=unit_tasks,
                vehicle_deploy=vehicle_deploy,
                chase_scenario=chase_scenario
            )

            messages.success(request, "تم إرسال التقديم بنجاح | انتظر اعلان النتيجة")
            return redirect("index")

        except IntegrityError:
            messages.error(request, "حصل خطأ، جرب تاني")
            return redirect("apply")

    return render(request, "apply/apply.html")