import os
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

        # Формат для имени файла
        file_time = now().strftime("%d.%m.%Y_%H-%M")
        # Формат для отображения в чеке
        display_time = now().strftime("%d.%m.%Y %H:%M")

        context = {
            'items': items,
            'total_price': total_price,
            'current_time': display_time,
        }

        # Генерация PDF с использованием Jinja2
        template = get_template('receipt_template.html')
        html = template.render(context)
        pdf_file_name = f'receipt_{file_time}.pdf'
        pdf_file_path = os.path.join('media', pdf_file_name)

        # Указываем путь к wkhtmltopdf
        path_to_wkhtmltopdf = os.getenv('WKHTMLTOPDF_PATH', default='/usr/local/bin/wkhtmltopdf')
        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
        pdfkit.from_string(html, pdf_file_path, configuration=config)

        # Генерация полного пути к PDF файлу
        pdf_url = request.build_absolute_uri(f'/media/{pdf_file_name}')

        # Генерация QR-кода
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(pdf_url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        qr_file_name = f'qrcode_{file_time}.png'
        img_file_path = os.path.join('media', qr_file_name)
        img.save(img_file_path)

        # Генерация полного пути к QR-коду
        qr_code_url = request.build_absolute_uri(f'/media/{qr_file_name}')

        return JsonResponse({'qr_code_url': qr_code_url})
