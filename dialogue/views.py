from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .boh_core import BOHCore


def dialogue(request):
    """View principal para o diálogo com BOH!"""
    return render(request, "dialogue/main.html")


def main(request):
    """View principal consolidada"""
    return render(request, "dialogue/main.html")


def index(request):
    """Redireciona para main"""
    return render(request, "dialogue/main.html")


@csrf_exempt
def api_dialogue(request):
    """API unificada para gerenciar o diálogo com BOH!"""
    if request.method == "GET":
        # Endpoint de saúde/teste para verificação de conectividade
        boh = BOHCore()
        return JsonResponse(
            {
                "status": "healthy",
                "message": "BOH Dialogue API está funcionando",
                "available_actions": [
                    "get_all_data",
                    "get_dialogue_item",
                    "advance_step",
                    "set_user_name",
                    "colorize_arrows",
                    "get_list_model",
                    "get_aux_art",
                    "get_expression",
                    "save_state",
                    "reset",
                ],
                "dialogue_steps": len(boh.dialogue_sequence),
                "expressions": len(boh.expressions),
                "list_models": len(boh.list_models),
                "aux_art": len(boh.aux_art),
            }
        )

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("action")
            boh = BOHCore()

            if action == "get_all_data":
                return JsonResponse(boh.get_all_data())

            elif action == "get_dialogue_item":
                step = data.get("step", boh.current_step)
                boh.current_step = step
                item = boh.get_current_dialogue_item()
                return JsonResponse({"item": item, "step": step})

            elif action == "advance_step":
                item = boh.advance_step()
                return JsonResponse({"item": item, "step": boh.current_step})

            elif action == "set_user_name":
                name = data.get("name", "")
                boh.set_user_name(name)
                return JsonResponse({"success": True, "name": boh.user_name})

            elif action == "colorize_arrows":
                text = data.get("text", "")
                colorized = boh.colorize_arrows(text)
                return JsonResponse({"colorized_text": colorized})

            elif action == "get_list_model":
                model_type = data.get("type", "basic")
                model = boh.get_list_model(model_type)
                return JsonResponse({"model": model})

            elif action == "get_aux_art":
                state = data.get("state", "normal")
                art = boh.get_aux_art(state)
                return JsonResponse({"art": art})

            elif action == "get_expression":
                expr_type = data.get("type", "idle")
                expression = boh.get_expression(expr_type)
                return JsonResponse({"expression": expression})

            elif action == "save_state":
                # Implementar salvamento de estado se necessário
                state_data = data.get("state", {})
                boh.from_json(state_data)
                return JsonResponse({"success": True})

            elif action == "reset":
                boh.reset()
                return JsonResponse({"success": True})

            else:
                return JsonResponse({"error": "Ação inválida"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método não permitido"}, status=405)
