import logging
from functools import wraps
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


logger = logging.getLogger(__name__)


def csrf_check(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args,**kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            # логгируем
            if 'CSRF' in str(e):
                logger.warning(f"CSRF validation error: {e}", extra={
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                    'path': request.path,
                    'method': request.method
                })
                # Возвращаем JSON для AJAX запросов
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'error': 'CSRF_TOKEN_EXPIRED',
                        'message': 'CSRF токен устарел',
                        'refresh_required': True
                    }, status=403)
                # Для обычных запросов - редирект
                else:
                    # from django.shortcuts import redirect
                    return redirect(request.path)
            raise e
    return _wrapped_view
