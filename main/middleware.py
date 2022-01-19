from .models import SavedProduct

def product_middleware(get_response):
    def middleware(request):
        request.saved_product = None
        if request.user.is_authenticated:
            saved_product = SavedProduct.objects.filter(user = request.user).values_list('product_id',flat=True)
            if saved_product:
                request.saved_product = saved_product
        response = get_response(request)
        return response
    return middleware


        