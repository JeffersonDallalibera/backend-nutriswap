from io import BytesIO
from flask import Response
from xhtml2pdf import pisa
from app.services.pessoa_service import criar_pessoa_pdf as pessoa_service_criar_pessoa_pdf


class PDFService:
    @staticmethod
    def generate_pdf(data):
        # Cria um buffer para armazenar o PDF em memória
        buffer = BytesIO()
        pessoa_data = pessoa_service_criar_pessoa_pdf(data['idPessoa'])

        # HTML para o PDF
        html = PDFService.render_html(data, pessoa_data)

        # Converte HTML para PDF
        pisa_status = pisa.CreatePDF(html, dest=buffer)

        # Move o buffer para o início
        buffer.seek(0)

        if pisa_status.err:
            return Response("Erro ao gerar PDF", status=500)

        return buffer

    @staticmethod
    def render_html(data, pessoa_data):
        # Monta o HTML
        meals_html = ""
        if 'refeicoes' in data:
            for refeicao in data['refeicoes']:
                meals_html += PDFService.draw_meal(refeicao)
        else:
            meals_html = "<p>Nenhuma refeição cadastrada.</p>"

        html = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                    }}
                    h1, h2, h3 {{
                        color: #333;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                </style>
            </head>
            <body>
                <h1>Plano de Dieta - NutriSwap</h1>
                <h2>Informações da Pessoa</h2>
                <table>
                    <tr><th>Nome</th><td>{pessoa_data['nome_pessoa']}</td></tr>
                    <tr><th>Idade</th><td>{pessoa_data['idade_pessoa']}</td></tr>
                    <tr><th>Peso</th><td>{pessoa_data['peso_pessoa']} kg</td></tr>
                    <tr><th>Altura</th><td>{pessoa_data['altura_pessoa']} cm</td></tr>
                    <tr><th>E-mail</th><td>{pessoa_data['email_pessoa']}</td></tr>
                    <tr><th>Telefone</th><td>{pessoa_data['telefone_pessoa']}</td></tr>
                    <tr><th>IMC</th><td>{pessoa_data['imc_pessoa']:.2f}</td></tr>
                </table>
                <h2>Refeições do Dia:</h2>
                {meals_html}
            </body>
        </html>
        """
        return html

    @staticmethod
    def draw_meal(refeicao):
        meal_html = f"<h3>{refeicao['tipo_refeicao'].capitalize()}: {refeicao['descricao']}</h3>"
        meal_html += "<table><tr><th>Alimento</th><th>Quantidade</th><th>Tipo</th></tr>"

        for alimento in refeicao['alimentos']:
            meal_html += f"<tr><td>{alimento['nome']}</td><td>{alimento['quantidade']}</td><td>{alimento['tipo']}</td></tr>"

        meal_html += "</table>"
        return meal_html
