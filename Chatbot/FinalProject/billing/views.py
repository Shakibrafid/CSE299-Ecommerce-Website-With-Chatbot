from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from xhtml2pdf import pisa

# FIXED: Changed from store.models to orders.models
from orders.models import Order 

@staff_member_required
def admin_invoice_pdf_view(request, order_id):
    """
    Generates a billing paper PDF exclusively for staff/admins from the admin panel.
    """
    # Fetches any order by ID so the admin can print it regardless of who bought it
    order = get_object_or_404(Order, id=order_id)
    
    template = get_template('invoices/bill.html')
    context = {
        'order': order,
        'items': order.items.all() # Correctly pulls your OrderItem related_name='items'
    }
    html_content = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    # Changing 'attachment' to 'inline' makes it open directly in a browser print tab
    response['Content-Disposition'] = f'inline; filename="invoice_{order.order_number}.pdf"'
    
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error generating PDF invoice.', status=500)
        
    return response
