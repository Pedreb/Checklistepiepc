import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
import io
import os
import base64

# Configuração da página
st.set_page_config(
    page_title="Checklist EPC/EPI - Rezende",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def get_base64_image(image_path):
    """Converte imagem para base64"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""


# CSS personalizado inspirado no exemplo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .main > div {
        padding-top: 2rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main-title {
        background: linear-gradient(135deg, #F7931E 0%, #000000 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(247, 147, 30, 0.3);
    }

    .main-title h1 {
        margin: 0;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
    }

    .main-title .subtitle {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 400;
    }

    .section-title {
        background: linear-gradient(135deg, #F7931E 0%, #000000 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(247, 147, 30, 0.2);
    }

    .section-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #F7931E 0%, #e8850c 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(247, 147, 30, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(247, 147, 30, 0.4);
    }

    .status-conforme {
        background: #d4edda;
        color: #155724;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 500;
        font-size: 0.8rem;
        text-align: center;
        margin: 0.2rem 0;
    }

    .status-nao-conforme {
        background: #f8d7da;
        color: #721c24;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 500;
        font-size: 0.8rem;
        text-align: center;
        margin: 0.2rem 0;
    }

    .status-na {
        background: #e2e3e5;
        color: #383d41;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 500;
        font-size: 0.8rem;
        text-align: center;
        margin: 0.2rem 0;
    }

    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        border-left: 4px solid #F7931E;
    }

    .item-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem;
        margin: 0.3rem 0;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 3px solid #F7931E;
    }

    .item-name {
        font-weight: 500;
        color: #333;
        flex: 1;
        font-size: 0.9rem;
    }

    .stSelectbox > label,
    .stTextInput > label,
    .stDateInput > label,
    .stTextArea > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #333;
        font-size: 0.9rem;
    }

    .category-header {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 1rem 0 0.5rem 0;
        font-weight: 600;
        font-size: 1rem;
    }

    @media (max-width: 768px) {
        .main-title h1 {
            font-size: 1.8rem;
        }
        .section-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


def load_logo():
    """Carrega a logo da empresa"""
    logo_path = r"C:\Users\Pedro Curry\OneDrive\Área de Trabalho\Rezende\MARKETING\__sitelogo__Logo Rezende.png"
    if os.path.exists(logo_path):
        return logo_path
    else:
        return None


def get_epc_items():
    """Lista de itens do checklist EPC organizados por categoria"""
    return {
        "Ferramentas Básicas": [
            "ALICATE BOMBA D'ÁGUA 12\"",
            "ALICATE HIDRAULICO COMPRESSÃO COM MATRIZES",
            "ARCO DE SERRA COMUM",
            "ARCO DE SERRA ISOLADO/SERRA PARA ARCO DE SERRA",
            "CHAVE AJUSTÁVEL INGLESA BOCA 25MM",
            "CHAVE AJUSTÁVEL INGLESA BOCA 35MM",
            "CHAVE ALLE 1/8 -9/16POL SX",
            "CHAVE FENDAR 6 X 150MM",
            "CHAVE FENDAR 8 X 150MM",
            "CHAVE DE BOCA 1/4 X 3 X 4 POL",
            "JOGO CHAVE ALLEN 1/8\" A 9/16\"",
            "JOGO CHAVE FIXA 8 PCS 1/4\" A 1.1/4\"",
            "MARRETA 1,5KG C/CABO",
            "FACÃO 20 POL."
        ],
        "Equipamentos de Segurança": [
            "ATERRAMENTO PARA VEÍCULO",
            "CONJUNTO DE ATERRAMENTO RÁPIDO E TEMPORÁRIO ATÉ 34",
            "CONJUNTO DE ATERRAMENTO RÁPIDO E TEMPORÁRIO SECUNDÁRIO",
            "CONJUNTO DE ATERRAMENTO BT PARA REDE MULTIPLEX",
            "DETECTOR DE PRESENÇA DE TENSÃO POR APROX. BT / MT / AT",
            "BANQUETA ISOLADA",
            "LENÇOL ISOLANTE P/BT",
            "LUVA DE BORRACHA CLASSE 2 / LUVA COBERTURA VAQUETA",
            "LUVA DE BORRACHA CLASSE 4"
        ],
        "Equipamentos de Elevação": [
            "BALDE DE LONA FUNDO DE COURO / PARA IÇAMENTO",
            "CINTA DE ELEVAÇÃO 3TON. X 20CM LARG. X 1,5MT COMP.",
            "CINTA DE ELEVAÇÃO 3TON. X 20CM LARG. X 2MT COMP.",
            "CINTA DE ELEVAÇÃO 2TON. X 20CM LARG. X 2MT COMP.",
            "CINTA TUBULAR TIPO ANEL PARA ELEVAÇÃO DE POSTA CAPA TR",
            "ROLDANA PARA ELEVAÇÃO DE MATERIAIS, COM GANCHO",
            "MOITÃO DUPLO 1500 DAN C/ 40MT DE CORDA",
            "MOSQUETÃO OVAL COMUM PARA IÇAMENTO DE MATERIAIS",
            "ROLDANA P/ LANÇAMENTO DE CABO C/ FIXAÇÃO NA CRUZETA"
        ],
        "Ferramentas Especializadas": [
            "ALAVANCA AÇO SEXTAVADA, 1500 MM",
            "ALICATE VOLT AMPERÍMETRO DE 20A - 1000A",
            "BASTÃO PEGA TUDO",
            "BASTÃO PODADOR DE GALHOS C/ CABEÇOTE UNIVERSAL",
            "CABEÇOTE PARA INSTALAÇÃO DE ESPAÇADORES",
            "CATRACA PARA TENSIONAR CABO COM ESTIRANTE DE NYLON",
            "FERRAMENTA P/ APLICAÇÃO DE CONECTOR TIPO CUNHA",
            "FERRAMENTA P/ OPERAÇÃO DE CHAVE C/ CARGA 25KV / 66A LOADBUSTER",
            "VARA DE MANOBRA TELESCÓPICA 5 ESTÁGIOS C/ CABEÇOTE"
        ],
        "Equipamentos de Trabalho": [
            "CAVALETE BOBINA",
            "CAVADEIRA AÇO COM CABO",
            "COLHER DE PEDREIRO 8 POL",
            "ENXADA C/CABO FERRO 1,80 MT",
            "ENXADADETA /CABO MADEIRA 1,5KG",
            "ESCADA FIBRA EXT. 5,40X9,60M",
            "ESCADA FIBRA EXT. 4,20X7.20M",
            "MOTOSSERRA SABRE 30,40,50",
            "PÁ QUADRADA GRANDE P/ JUNTAR C/ CABO DE MADEIRA EM \"Y\"",
            "VASSOURAM GARI GRANDE"
        ],
        "Acessórios e Materiais": [
            "BOLSA DE LONA PARA EPI E FERRAMENTAS",
            "BOLSA DE BASTÃO PEGA TUDO",
            "BANDEIROLA",
            "CONE DE SINALIZAÇÃO GRANDE COM PINTURA FOSFORECENTE",
            "CORDA ESTÁTICA CAPA E ALMA 12MM 22KN \"LINHA DE VIDA 144 METROS",
            "CORDA PARA IÇAR FERRAMENTAS E MATERIAIS 10MM 43 METROS",
            "DEPÓSITO PARA ÁGUA 10L",
            "ENCERADO 6 X 5 M",
            "ESCOVA EM \"V\" PARA LIMPEZA DE CONDUTOR COM ENCAIXE",
            "GARRAFA TÉRMICA 12LT",
            "KIT PRIMEIROS SOCORROS",
            "LÂMINA PARA ARCO DE SERRA 24D",
            "PLACA SINALIZAÇÃO \"ATENÇÃO! NÃO OPERE ESTE EQUIPAMENTO\"",
            "PLACA SINALIZAÇÃO \"NÃO LIGAR, HOMENS NA LINHA\"",
            "PRANCHETA OFÍCIO C/ PRENDEDOR PLÁST.",
            "TRENA DE FITA FIBRA 50MT"
        ]
    }


def get_epi_items():
    """Lista de itens do checklist EPI organizados por categoria"""
    return {
        "Proteção da Cabeça": [
            "Capacete de segurança classe B",
            "Jugular para capacete"
        ],
        "Proteção dos Olhos e Face": [
            "Óculos de segurança incolor",
            "Óculos de segurança cinza ou fumê",
            "Óculos de sobreposição (para quem usa óculos de grau)",
            "Balaclava simples",
            "Balaclava Antichamas",
            "Protetor facial contra arco elétrico"
        ],
        "Proteção Respiratória": [
            "Respirador descartável PFF1",
            "Respirador descartável PFF2"
        ],
        "Proteção Auditiva": [
            "Protetor auricular tipo plug (descartável)",
            "Protetor auricular tipo plug com cordão",
            "Protetor auricular tipo concha (abafador)"
        ],
        "Proteção do Tronco e Corpo": [
            "Camisa de manga longa anti-chamas",
            "Calça anti-chamas",
            "Colete refletivo de alta visibilidade",
            "Colete Salva vidas"
        ],
        "Proteção das Mãos e Braços": [
            "Luva de vaqueta (manuseio de materiais)",
            "Luva de raspa (solda e corte)",
            "Luva isolante classe 0 (até 1.000 V)",
            "Luva isolante classe 2 (até 17.000 V)",
            "Luva isolante classe 4 (até 36.000 V)",
            "Luva de cobertura de vaqueta (uso sobre as isolantes)",
            "Manga de raspa (proteção do braço)",
            "Manga isolante classe 2 (até 17.000 V)"
        ],
        "Proteção das Pernas": [
            "Perneira de raspa (trabalho com motosserra e ferramentas de corte)",
            "Perneira contra animais peçonhentos (mata e roçada)"
        ],
        "Proteção dos Pés": [
            "Botina de segurança com biqueira de aço",
            "Botina de segurança com biqueira de composite (NR 10)",
            "Bota dielétrica (classe elétrica)",
            "Bota de PVC antiderrapante (chuva, lama e herbicidas)"
        ],
        "Proteção Contra Quedas": [
            "Cinturão tipo paraquedista",
            "Cinto paraquedista com talabarte",
            "Talabarte ajustável para posicionamento",
            "Linha de vida vertical com trava-quedas",
            "Trava-quedas retrátil",
            "Conectores mosquetões (trava dupla automática)"
        ],
        "Atividades Rurais": [
            "Protetor solar",
            "Repelente contra insetos"
        ],
        "Itens Complementares": [
            "Capacete com viseira integrada contra arco elétrico",
            "Protetor lombar (ergonomia – carga e descarga)",
            "Capa de chuva PVC (isolante e visibilidade em obras externas)"
        ]
    }


def create_pdf_epc(data, info_data):
    """Cria PDF do checklist EPC com layout moderno"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.8 * inch, leftMargin=0.5 * inch, rightMargin=0.5 * inch)

    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=16,
        textColor=HexColor('#000000'),
        fontName='Helvetica-Bold',
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=HexColor('#F7931E'),
        fontName='Helvetica-Bold',
        spaceAfter=10
    )

    elements = []

    # Logo (se disponível)
    logo_path = load_logo()
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=2 * inch, height=1 * inch)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 12))
        except:
            pass

    # Título
    title = Paragraph("Checklist - Equipamentos de Proteção Coletiva (EPCs)", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Informações gerais
    info_table_data = [
        ['Local:', info_data.get('local', ''), 'Data:', info_data.get('data', ''), 'Status Geral'],
        ['Empresa:', info_data.get('empresa', ''), 'Placa:', info_data.get('placa', ''), 'EPCs'],
        ['Veículo:', info_data.get('veiculo', ''), 'Modelo:', info_data.get('modelo', ''), ''],
        ['Matrícula:', info_data.get('matricula', ''), 'Colaborador:', info_data.get('colaborador', ''), ''],
        ['Função:', info_data.get('funcao', ''), 'Responsável:', info_data.get('responsavel', ''), '']
    ]

    page_width = A4[0] - 1 * inch
    col_widths = [page_width * 0.15, page_width * 0.2, page_width * 0.15, page_width * 0.25, page_width * 0.25]

    info_table = Table(info_table_data, colWidths=col_widths)
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (4, 0), (4, 1), HexColor('#F7931E')),
        ('TEXTCOLOR', (4, 0), (4, 1), colors.white),
        ('FONTNAME', (4, 0), (4, 1), 'Helvetica-Bold'),
        ('ALIGN', (4, 0), (4, 1), 'CENTER'),
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Legenda
    legenda = Paragraph(
        "Legenda: A = Bom | B = Solicitar Providências | C = Não Liberar | N/A = Não se Aplica",
        styles['Normal'])
    elements.append(legenda)
    elements.append(Spacer(1, 15))

    # Itens por categoria
    epc_categories = get_epc_items()
    for categoria, itens in epc_categories.items():
        # Título da categoria
        elements.append(Paragraph(categoria, section_style))

        # Tabela dos itens da categoria
        table_data = [['Descrição do Material', 'A', 'B', 'C', 'N/A']]

        for item in itens:
            status = data.get(item, '')
            row = [item, '', '', '', '', '']
            if status == 'A':
                row[1] = 'X'
            elif status == 'B':
                row[2] = 'X'
            elif status == 'C':
                row[3] = 'X'
            elif status == 'N/A':
                row[4] = 'X'
            table_data.append(row)

        cat_col_widths = [page_width * 0.6, page_width * 0.08, page_width * 0.08, page_width * 0.08, page_width * 0.08,
                          page_width * 0.08]

        cat_table = Table(table_data, colWidths=cat_col_widths)
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F7931E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(cat_table)
        elements.append(Spacer(1, 10))

    # Observações
    elements.append(Spacer(1, 20))
    obs_text = f"Observações: {info_data.get('observacoes', '')}"
    elements.append(Paragraph(obs_text, styles['Normal']))
    elements.append(Spacer(1, 30))

    # Assinaturas
    elements.append(Paragraph("ASSINATURAS", section_style))
    sig_table = Table([
        ['Responsável pela Inspeção', 'Operador'],
        ['_' * 30, '_' * 30],
        [f"Data: {info_data.get('data', '')}", f"Data: {info_data.get('data', '')}"]
    ], colWidths=[2.75 * inch, 2.75 * inch])

    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, 1), 20)
    ]))

    elements.append(sig_table)

    # Rodapé
    elements.append(Spacer(1, 30))
    footer_text = f"Documento gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} | Sistema Rezende Energia"
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey,
                                  alignment=TA_CENTER)
    elements.append(Paragraph(footer_text, footer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def create_pdf_epi(data, info_data):
    """Cria PDF do checklist EPI com layout moderno"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.8 * inch, leftMargin=0.5 * inch, rightMargin=0.5 * inch)

    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=16,
        textColor=HexColor('#000000'),
        fontName='Helvetica-Bold',
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=HexColor('#F7931E'),
        fontName='Helvetica-Bold',
        spaceAfter=10
    )

    elements = []

    # Logo (se disponível)
    logo_path = load_logo()
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=2 * inch, height=1 * inch)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 12))
        except:
            pass

    # Título
    title = Paragraph("Checklist - Equipamentos de Proteção Individual (EPIs)", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Informações gerais (mesmo layout do EPC)
    info_table_data = [
        ['Local:', info_data.get('local', ''), 'Data:', info_data.get('data', ''), 'Status Geral'],
        ['Empresa:', info_data.get('empresa', ''), 'Placa:', info_data.get('placa', ''), 'EPIs'],
        ['Veículo:', info_data.get('veiculo', ''), 'Modelo:', info_data.get('modelo', ''), ''],
        ['Matrícula:', info_data.get('matricula', ''), 'Colaborador:', info_data.get('colaborador', ''), ''],
        ['Função:', info_data.get('funcao', ''), 'Responsável:', info_data.get('responsavel', ''), '']
    ]

    page_width = A4[0] - 1 * inch
    col_widths = [page_width * 0.15, page_width * 0.2, page_width * 0.15, page_width * 0.25, page_width * 0.25]

    info_table = Table(info_table_data, colWidths=col_widths)
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (4, 0), (4, 1), HexColor('#F7931E')),
        ('TEXTCOLOR', (4, 0), (4, 1), colors.white),
        ('FONTNAME', (4, 0), (4, 1), 'Helvetica-Bold'),
        ('ALIGN', (4, 0), (4, 1), 'CENTER'),
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Legenda
    legenda = Paragraph(
        "Legenda: C = Conforme | NC = Não Conforme | NR = Não Recebeu | N/A = Não se Aplica",
        styles['Normal'])
    elements.append(legenda)
    elements.append(Spacer(1, 15))

    # Itens por categoria
    epi_categories = get_epi_items()
    for categoria, itens in epi_categories.items():
        # Título da categoria
        elements.append(Paragraph(categoria, section_style))

        # Tabela dos itens da categoria
        table_data = [['Descrição do Material', 'C', 'NC', 'NR', 'N/A']]

        for item in itens:
            status = data.get(item, '')
            row = [item, '', '', '', '', '']
            if status == 'C':
                row[1] = 'X'
            elif status == 'NC':
                row[2] = 'X'
            elif status == 'NR':
                row[3] = 'X'
            elif status == 'N/A':
                row[4] = 'X'
            table_data.append(row)

        cat_col_widths = [page_width * 0.58, page_width * 0.084, page_width * 0.084, page_width * 0.084,
                          page_width * 0.084, page_width * 0.084]

        cat_table = Table(table_data, colWidths=cat_col_widths)
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F7931E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(cat_table)
        elements.append(Spacer(1, 10))

    # Observações
    elements.append(Spacer(1, 20))
    obs_text = f"Observações: {info_data.get('observacoes', '')}"
    elements.append(Paragraph(obs_text, styles['Normal']))
    elements.append(Spacer(1, 30))

    # Assinaturas
    elements.append(Paragraph("ASSINATURAS", section_style))
    sig_table = Table([
        ['Responsável pela Inspeção', 'Operador'],
        ['_' * 30, '_' * 30],
        [f"Data: {info_data.get('data', '')}", f"Data: {info_data.get('data', '')}"]
    ], colWidths=[2.75 * inch, 2.75 * inch])

    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, 1), 20)
    ]))

    elements.append(sig_table)

    # Rodapé
    elements.append(Spacer(1, 30))
    footer_text = f"Documento gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} | Sistema Rezende Energia"
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey,
                                  alignment=TA_CENTER)
    elements.append(Paragraph(footer_text, footer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def create_checklist_section(title, items_dict, section_key, status_options):
    """Cria uma seção do checklist com design moderno"""
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        all_items_data = {}

        for categoria, itens in items_dict.items():
            st.markdown(f'<div class="category-header">{categoria}</div>', unsafe_allow_html=True)

            for item in itens:
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f'<div class="item-name">{item}</div>', unsafe_allow_html=True)

                with col2:
                    status = st.selectbox(
                        "Status",
                        [""] + status_options,
                        key=f"{section_key}_{item}",
                        label_visibility="collapsed"
                    )

                    all_items_data[item] = status

                    # Indicador visual do status
                    if status == status_options[0]:  # Primeira opção (Conforme/A)
                        st.markdown('<div class="status-conforme">Conforme</div>', unsafe_allow_html=True)
                    elif status == status_options[1]:  # Segunda opção (Não Conforme/B)
                        st.markdown('<div class="status-nao-conforme">Não Conforme</div>', unsafe_allow_html=True)
                    elif status == "N/A":
                        st.markdown('<div class="status-na">N/A</div>', unsafe_allow_html=True)

        # Campo de observações
        st.markdown("---")
        observacoes = st.text_area(f"Observações - {title}:", key=f"{section_key}_obs", height=100)

        st.markdown('</div>', unsafe_allow_html=True)

        return all_items_data, observacoes


def main():
    # Inicializar session state
    if 'checklist_data' not in st.session_state:
        st.session_state.checklist_data = {}

    # Título principal com logo
    logo_path = load_logo()
    logo_base64 = ""
    if logo_path:
        logo_base64 = get_base64_image(logo_path)

    st.markdown(f'''
    <div class="main-title" style="display: flex; align-items: center; justify-content: center;">
        <img src="data:image/png;base64,{logo_base64}" 
             alt="Logo Rezende" style="height: 60px; margin-right: 2rem; filter: brightness(0) invert(1);">
        <div>
            <h1>Sistema de Checklist EPC/EPI</h1>
            <p class="subtitle">Equipamentos de Proteção Coletiva e Individual - Rezende Energia</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Sidebar com informações
    with st.sidebar:
        st.markdown("### Informações do Sistema")

        epc_items = get_epc_items()
        epi_items = get_epi_items()
        total_epc = sum(len(items) for items in epc_items.values())
        total_epi = sum(len(items) for items in epi_items.values())

        st.info(f"**EPCs:** {total_epc} itens")
        st.info(f"**EPIs:** {total_epi} itens")
        st.success("**Status:** Online")
        st.markdown("**Versão:** 2.0")

        if st.button("Limpar Formulário", type="secondary"):
            st.session_state.checklist_data = {}
            st.rerun()

    # Navegação por tabs
    tab1, tab2 = st.tabs(["Checklist EPC", "Checklist EPI"])

    with tab1:
        # Dados da inspeção EPC
        st.markdown('<div class="section-title">DADOS DA INSPEÇÃO - EPC</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                local_epc = st.text_input("Local:", key="epc_local")
                empresa_epc = st.text_input("Empresa:", value="Rezende Energia", key="epc_empresa")

            with col2:
                data_epc = st.date_input("Data:", datetime.now(), key="epc_data")
                placa_epc = st.text_input("Placa do Veículo:", key="epc_placa")

            with col3:
                veiculo_epc = st.text_input("Veículo/Modelo:", key="epc_veiculo")
                matricula_epc = st.text_input("Matrícula:", key="epc_matricula")

            col4, col5 = st.columns(2)

            with col4:
                colaborador_epc = st.text_input("Nome do Colaborador:", key="epc_colaborador")

            with col5:
                funcao_epc = st.text_input("Função/Cargo:", key="epc_funcao")

            st.markdown('</div>', unsafe_allow_html=True)

        # Checklist EPC
        epc_data, epc_obs = create_checklist_section(
            "CHECKLIST - EQUIPAMENTOS DE PROTEÇÃO COLETIVA",
            get_epc_items(),
            "epc",
            ["A", "B", "C", "N/A"]
        )

        # Resultado e responsável
        st.markdown('<div class="section-title">RESULTADO E RESPONSABILIDADE</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                resultado_epc = st.radio(
                    "Resultado da Inspeção:",
                    ["Aprovado", "Reprovado", "Aprovado com Restrições"],
                    key="epc_resultado",
                    horizontal=True
                )

            with col2:
                responsavel_epc = st.text_input("Responsável pela Inspeção:", key="epc_responsavel")

            # Estatísticas
            st.markdown("### Estatísticas da Inspeção")

            col1, col2, col3, col4 = st.columns(4)

            bom = sum(1 for status in epc_data.values() if status == "A")
            solicitar = sum(1 for status in epc_data.values() if status == "B")
            nao_liberar = sum(1 for status in epc_data.values() if status == "C")
            na = sum(1 for status in epc_data.values() if status == "N/A")

            with col1:
                st.markdown(
                    f'<div class="metric-card"><h3 style="color: #28a745; margin: 0;">{bom}</h3><p style="margin: 0;">Bom</p></div>',
                    unsafe_allow_html=True)

            with col2:
                st.markdown(
                    f'<div class="metric-card"><h3 style="color: #ffc107; margin: 0;">{solicitar}</h3><p style="margin: 0;">Solicitar</p></div>',
                    unsafe_allow_html=True)

            with col3:
                st.markdown(
                    f'<div class="metric-card"><h3 style="color: #dc3545; margin: 0;">{nao_liberar}</h3><p style="margin: 0;">Não Liberar</p></div>',
                    unsafe_allow_html=True)

            with col4:
                st.markdown(
                    f'<div class="metric-card"><h3 style="color: #17a2b8; margin: 0;">{na}</h3><p style="margin: 0;">N/A</p></div>',
                    unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # Botão para gerar PDF EPC
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            if st.button("Gerar PDF - EPC", type="primary", use_container_width=True):
                if responsavel_epc and any(epc_data.values()):
                    info_data_epc = {
                        'local': local_epc,
                        'data': data_epc.strftime('%d/%m/%Y'),
                        'empresa': empresa_epc,
                        'placa': placa_epc,
                        'veiculo': veiculo_epc,
                        'matricula': matricula_epc,
                        'colaborador': colaborador_epc,
                        'funcao': funcao_epc,
                        'responsavel': responsavel_epc,
                        'observacoes': epc_obs,
                        'resultado': resultado_epc
                    }

                    try:
                        with st.spinner("Gerando PDF..."):
                            pdf_buffer = create_pdf_epc(epc_data, info_data_epc)

                            filename = f"Checklist_EPC_{data_epc.strftime('%Y%m%d')}_{colaborador_epc.replace(' ', '_') if colaborador_epc else 'Usuario'}.pdf"

                            st.download_button(
                                label="Download PDF EPC",
                                data=pdf_buffer.getvalue(),
                                file_name=filename,
                                mime="application/pdf",
                                type="primary",
                                use_container_width=True
                            )
                            st.success("PDF gerado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao gerar PDF: {str(e)}")
                else:
                    st.error("Preencha o responsável e pelo menos um item do checklist.")

    with tab2:
        # Dados da inspeção EPI
        st.markdown('<div class="section-title">DADOS DA INSPEÇÃO - EPI</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                empresa_epi = st.text_input("Empresa:", value="Rezende Energia", key="epi_empresa")
                colaborador_epi = st.text_input("Nome do Colaborador:", key="epi_colaborador")


            with col2:
                data_epi = st.date_input("Data:", datetime.now(), key="epi_data")
                local_epi = st.text_input("Local:", key="epi_local")

            with col3:
                matricula_epi = st.text_input("Matrícula:", key="epi_matricula")
                funcao_epi = st.text_input("Função/Cargo:", key="epi_funcao")

            st.markdown('</div>', unsafe_allow_html=True)

        # Checklist EPI
        epi_data, epi_obs = create_checklist_section(
            "CHECKLIST - EQUIPAMENTOS DE PROTEÇÃO INDIVIDUAL",
            get_epi_items(),
            "epi",
            ["C", "NC", "NR", "N/A"]
        )

        # Resultado e responsável
        st.markdown('<div class="section-title">RESULTADO E RESPONSABILIDADE</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                resultado_epi = st.radio(
                    "Resultado da Inspeção:",
                    ["Aprovado", "Reprovado", "Aprovado com Restrições"],
                    key="epi_resultado",
                    horizontal=True
                )

            with col2:
                responsavel_epi = st.text_input("Responsável pela Inspeção:", key="epi_responsavel")

            # Estatísticas
            st.markdown("### Estatísticas da Inspeção")

            col1, col2, col3, col4 = st.columns(4)

            conforme = sum(1 for status in epi_data.values() if status == "C")
            nao_conforme = sum(1 for status in epi_data.values() if status == "NC")
            nao_recebeu = sum(1 for status in epi_data.values() if status == "NR")
            na_epi = sum(1 for status in epi_data.values() if status == "N/A")

            with col1:
                st.markdown(
                    f'<div class="metric-card"><h3 style="color: #28a745; margin: 0;">{conforme}</h3><p style="margin: 0;">Conforme</p></div>',
                    unsafe_allow_html=True)

            with col2:
                st.markdown(
                    f'<div class="metric-card"><h3 style="color: #dc3545; margin: 0;">{nao_conforme}</h3><p style="margin: 0;">Não Conforme</p></div>',
                    unsafe_allow_html=True)

            with col3:
                st.markdown(
                    f'<div class="metric-card"><h3 style="color: #ffc107; margin: 0;">{nao_recebeu}</h3><p style="margin: 0;">Não Recebeu</p></div>',
                    unsafe_allow_html=True)


            with col4:
                st.markdown(
                    f'<div class="metric-card"><h3 style="color: #17a2b8; margin: 0;">{na_epi}</h3><p style="margin: 0;">N/A</p></div>',
                    unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # Botão para gerar PDF EPI
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            if st.button("Gerar PDF - EPI", type="primary", use_container_width=True):
                if responsavel_epi and any(epi_data.values()):
                    info_data_epi = {
                        'local': local_epi,
                        'data': data_epi.strftime('%d/%m/%Y'),
                        'empresa': empresa_epi,
                        'placa': '',  # Removido para EPI
                        'veiculo': '',  # Removido para EPI
                        'matricula': matricula_epi,
                        'colaborador': colaborador_epi,
                        'funcao': funcao_epi,
                        'responsavel': responsavel_epi,
                        'observacoes': epi_obs,
                        'resultado': resultado_epi
                    }

                    try:
                        with st.spinner("Gerando PDF..."):
                            pdf_buffer = create_pdf_epi(epi_data, info_data_epi)

                            filename = f"Checklist_EPI_{data_epi.strftime('%Y%m%d')}_{colaborador_epi.replace(' ', '_') if colaborador_epi else 'Usuario'}.pdf"

                            st.download_button(
                                label="Download PDF EPI",
                                data=pdf_buffer.getvalue(),
                                file_name=filename,
                                mime="application/pdf",
                                type="primary",
                                use_container_width=True
                            )
                            st.success("PDF gerado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao gerar PDF: {str(e)}")
                else:
                    st.error("Preencha o responsável e pelo menos um item do checklist.")


if __name__ == "__main__":
    main()