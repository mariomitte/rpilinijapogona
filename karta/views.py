from easy_pdf.views import PDFTemplateView

class HelloPDFView(PDFTemplateView):
    template_name = 'karta/karta.html'
