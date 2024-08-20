import pdfkit
import qrcode
from django.http import JsonResponse
from django.template.loader import get_template
from django.utils.timezone import now
from rest_framework.views import APIView
from .models import Item


class CashMachineView(APIView):
    def post(self, request, *args, **kwargs):
        item_ids = request.data.get('items', [])
        items = Item.objects.filter(id__in=item_ids)
        total_price = sum(item.price for item in items)
        current_time = now().strftime("%d.%m.%Y %H:%M")
        context = {
            'items': items,
            'total_price': total_price,
            'current_time': current_time
        }

        # Генерация PDF с использованием Jinja2
        template = get_template('receipt_template.html')
        html = template.render(context)
        pdf_file_path = f'media/receipt_{current_time}.pdf'
        pdfkit.from_string(html, pdf_file_path)

        # Генерация QR-кода
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(pdf_file_path)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img_file_path = f'media/qrcode_{current_time}.png'
        img.save(img_file_path)

        return JsonResponse({'qr_code_url': img_file_path})
