from flask import Blueprint, make_response, request
from app.services.pdf_service import PDFService

bp = Blueprint('pdf', __name__)

@bp.route('/gerar_dieta', methods=['POST'])
def generate_pdf():
    data = request.get_json()

    # Verifica se os dados recebidos estão completos
    if not data or 'idPessoa' not in data or 'refeicoes' not in data:
        return {"error": "Dados incompletos"}, 400

    # Gera o PDF com o serviço
    pdf_buffer = PDFService.generate_pdf(data)

    # Cria uma resposta Flask com o PDF
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=nutriswap_report.pdf'

    return response
