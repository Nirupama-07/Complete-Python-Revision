import subprocess
import sys

from django.shortcuts import render,get_object_or_404
from .models import Chapters, CodingQuestion
from django.http import JsonResponse


# Create your views here.
def home(request):
    chapters=Chapters.objects.all()
    return render(request,'home.html',{"chapters":chapters})

def chapter(request, chapter_number):
    chapter = get_object_or_404(
        Chapters,
        number=chapter_number
    )

    chapters = Chapters.objects.all().order_by("number")

    return render(request, "chapter.html", {
        "chapter": chapter,
        "chapters": chapters
    })

def run_code(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Only POST requests are allowed."
        }, status=400)

    code = request.POST.get("code", "")
    coding_id = request.POST.get("coding_id")

    if not code.strip():
        return JsonResponse({
            "success": False,
            "error": "Please write some Python code."
        })

    if len(code) > 5000:
        return JsonResponse({
            "success": False,
            "error": "Code is too long."
        })

    try:
        coding_question = CodingQuestion.objects.get(
            id=coding_id
        )
    except CodingQuestion.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Coding question not found."
        }, status=404)

    try:

        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=3,
            shell=False
        )

        if result.returncode != 0:
            return JsonResponse({
                "success": False,
                "error": result.stderr
            })

        user_output = result.stdout.strip()
        expected_output = coding_question.expected_output.strip()

        is_correct = user_output == expected_output

        return JsonResponse({
            "success": True,
            "output": user_output,
            "correct": is_correct
        })

    except subprocess.TimeoutExpired:

        return JsonResponse({
            "success": False,
            "error": "Execution timed out."
        })

    except Exception as error:

        return JsonResponse({
            "success": False,
            "error": str(error)
        })

def check_answer(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Only POST requests are allowed."
        }, status=400)

    answer = request.POST.get("answer", "")
    coding_id = request.POST.get("coding_id")

    try:
        coding_question = CodingQuestion.objects.get(
            id=coding_id
        )
    except CodingQuestion.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Coding question not found."
        }, status=404)

    user_answer = answer.strip().replace("\r\n", "\n")
    expected_answer = coding_question.expected_output.strip().replace("\r\n", "\n")

    if user_answer == expected_answer:

        return JsonResponse({
            "success": True,
            "correct": True,
            "message": "✅ Correct!"
        })

    return JsonResponse({
        "success": True,
        "correct": False,
        "message": "❌ Incorrect!"
    })