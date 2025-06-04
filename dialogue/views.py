from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .boh_manager import BOHDialogueManager


def dialogue(request):
    """View principal para o diálogo com BOH!"""
    return render(request, "dialogue/index_complete.html")


def test_pause(request):
    """View de teste para sistema de pausas"""
    return render(request, "dialogue/test_pause.html")


def debug(request):
    """View de debug para diagnosticar problemas"""
    return render(request, "dialogue/debug.html")


@csrf_exempt
def api_dialogue_state(request):
    """API para gerenciar o estado do diálogo"""
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")

        manager = BOHDialogueManager()

        if action == "get_sequence":
            return JsonResponse(
                {
                    "sequence": manager.dialogue_sequence,
                    "expressions": manager.expressions,
                }
            )

        elif action == "get_list_models":
            return JsonResponse(manager.get_list_models())

        elif action == "get_aux_ascii":
            state = data.get("state", "normal")
            return JsonResponse({"ascii": manager.get_aux_ascii(state)})

        elif action == "colorize_arrows":
            text = data.get("text", "")
            return JsonResponse({"colorized_text": manager.colorize_arrows(text)})

    return JsonResponse({"error": "Method not allowed"}, status=405)
