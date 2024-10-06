from io import BytesIO
from flask import Response
from xhtml2pdf import pisa
from app.services.pessoa_service import buscar_pessoa_pdf as pessoa_service_buscar_pessoa_pdf

class PDFService:
    @staticmethod
    def generate_pdf(data):
        buffer = BytesIO()
        pessoa_data = pessoa_service_buscar_pessoa_pdf(data['idPessoa'])
        html = PDFService.render_html(data, pessoa_data)
        pisa_status = pisa.CreatePDF(html, dest=buffer)
        buffer.seek(0)

        if pisa_status.err:
            return Response("Erro ao gerar PDF", status=500)

        return buffer

    @staticmethod
    def render_html(data, pessoa_data):
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
                        color: #333;
                    }}
                    h1, h2 {{
                        text-align: center;
                        color: #4CAF50;
                    }}
                    h3 {{
                        color: #333;
                        margin-top: 20px;
                        margin-bottom: 10px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                        overflow-wrap: break-word;
                        word-wrap: break-word;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    .person-info th {{
                        width: 30%;
                    }}
                    .person-info td {{
                        width: 70%;
                        text-align: left;
                    }}
                    .meal-table {{
                        width: 100%;
                        table-layout: fixed;
                    }}
                    .meal-table th {{
                        text-align: center;
                    }}
                    .meal-table td {{
                        text-align: left;
                        vertical-align: top;
                    }}
                    .meal-table th.alimento, .meal-table td.alimento {{
                        width: 60%;
                    }}
                    .meal-table th.quantidade, .meal-table td.quantidade {{
                        width: 20%;
                    }}
                    .meal-table th.tipo, .meal-table td.tipo {{
                        width: 20%;
                    }}
                    .equivalente {{
                        padding-left: 20px;
                        font-style: italic;
                    }}
                </style>
            </head>
            <body>
                <h1>Plano de Dieta - NutriSwap</h1>
                <h2>Informações da Pessoa</h2>
                <table class="person-info">
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
        meal_html = f"<h3>{refeicao['nome']}</h3>"
        meal_html += """
            <table class="meal-table">
                <tr>
                    <th class="alimento">Alimento</th>
                    <th class="quantidade">Quantidade</th>
                    <th class="tipo">Tipo</th>
                </tr>
        """

        for alimento in refeicao['alimentos']:
            meal_html += f"""
                <tr>
                    <td class="alimento">{alimento['nome']}</td>
                    <td class="quantidade">{alimento['quantidade']}</td>
                    <td class="tipo">{alimento['tipoQuantidade']}</td>
                </tr>
            """

            if 'equivalente' in alimento:
                for eq in alimento['equivalente']:
                    alimento_eq = eq['alimento']['nome']
                    quantidade_ajustada = eq['quantidade_ajustada']
                    meal_html += f"""
                        <tr>
                            <td class="alimento equivalente">{alimento_eq} (equivalente)</td>
                            <td class="quantidade">{quantidade_ajustada:.2f}</td>
                            <td class="tipo">{alimento['tipoQuantidade']}</td>
                        </tr>
                    """

        meal_html += "</table>"
        return meal_html