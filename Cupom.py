# App.py - Cupom Fiscal (Versão Profissional - Portfólio)
import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Cupom Fiscal - UNOPAR (Portfólio)", page_icon="🏷️", layout="centered")

# ---------- Estilo ----------
st.markdown(
    """
    <style>
    .big-title { font-size:28px; font-weight:700; color:#0B3D91; }
    .muted { color: #444; }
    .card { background: #fff; padding: 16px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.06);}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='big-title'>🏷️ Cupom Fiscal - UNOPAR Vila Velha</div>", unsafe_allow_html=True)
st.markdown("<div class='muted'>Sistema minimalista para portfólio — versão profissional</div>", unsafe_allow_html=True)
st.write("----")

# ---------- Dados do cliente ----------
with st.form(key="cliente_form"):
    st.subheader("Dados do Cliente")
    nome = st.text_input("Nome completo")
    idade = st.text_input("Idade")
    cpf = st.text_input("CPF")
    pagamento = st.selectbox("Forma de pagamento", ["Dinheiro", "Cartão de Débito", "Cartão de Crédito", "Pix", "Outro"])
    st.write("---")
    st.subheader("Produtos (3 itens)")
    # Produto 1
    produto1 = st.text_input("Produto 1 - Nome", key="p1")
    preço1 = st.number_input("Produto 1 - Preço (R$)", min_value=0.0, format="%.2f", key="pr1")
    quantidade1 = st.number_input("Produto 1 - Quantidade", min_value=0, step=1, key="q1")
    # Produto 2
    produto2 = st.text_input("Produto 2 - Nome", key="p2")
    preço2 = st.number_input("Produto 2 - Preço (R$)", min_value=0.0, format="%.2f", key="pr2")
    quantidade2 = st.number_input("Produto 2 - Quantidade", min_value=0, step=1, key="q2")
    # Produto 3
    produto3 = st.text_input("Produto 3 - Nome", key="p3")
    preço3 = st.number_input("Produto 3 - Preço (R$)", min_value=0.0, format="%.2f", key="pr3")
    quantidade3 = st.number_input("Produto 3 - Quantidade", min_value=0, step=1, key="q3")

    st.write("---")
    desconto = st.number_input("Desconto (%)", min_value=0.0, max_value=100.0, format="%.2f", value=0.0)
    submitted = st.form_submit_button("Gerar Cupom")

if submitted:
    # ---------- Cálculos ----------
    subtotal1 = preço1 * quantidade1
    subtotal2 = preço2 * quantidade2
    subtotal3 = preço3 * quantidade3
    total_bruto = subtotal1 + subtotal2 + subtotal3
    valor_desconto = total_bruto * (desconto / 100)
    total_final = total_bruto - valor_desconto

    # ---------- Mostrar cupom ----------
    st.markdown("### 📄 Cupom Fiscal")
    st.markdown("**Cliente:** " + (nome if nome else "[não informado]"))
    st.markdown(f"**Idade:** {idade}    **CPF:** {cpf}    **Pagamento:** {pagamento}")
    st.write("")

    # Tabela dos produtos
    data = {
        "Produto": [produto1, produto2, produto3],
        "Qtd": [int(quantidade1), int(quantidade2), int(quantidade3)],
        "Preço (R$)": [float(preço1), float(preço2), float(preço3)],
        "Subtotal (R$)": [float(subtotal1), float(subtotal2), float(subtotal3)]
    }
    df = pd.DataFrame(data)
    st.table(df.style.format({"Preço (R$)": "{:.2f}", "Subtotal (R$)": "{:.2f}"}))

    st.markdown("---")
    st.write(f"**Total bruto:** R$ {total_bruto:.2f}")
    st.write(f"**Desconto:** {desconto:.2f}%  (R$ {valor_desconto:.2f})")
    st.write(f"**Total final:** R$ {total_final:.2f}")
    st.markdown("---")

    # ---------- Preparar arquivos para download ----------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"cupom_{timestamp}"

    # CSV
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False, float_format="%.2f")
    csv_bytes = csv_buffer.getvalue()

    # TXT (cupom formatado)
    txt_lines = []
    txt_lines.append("-------------- CUPOM FISCAL --------------")
    txt_lines.append(f"Cliente: {nome}")
    txt_lines.append(f"Idade: {idade}    CPF: {cpf}    Pagamento: {pagamento}")
    txt_lines.append("")
    for i in range(3):
        prod = data["Produto"][i] or "[--]"
        qtd = data["Qtd"][i]
        preco = data["Preço (R$)"][i]
        sub = data["Subtotal (R$)"][i]
        txt_lines.append(f"{prod}  |  Qtd: {qtd}  |  Preço: R${preco:.2f}  |  Subtotal: R${sub:.2f}")
    txt_lines.append("------------------------------------------")
    txt_lines.append(f"Total bruto: R${total_bruto:.2f}")
    txt_lines.append(f"Desconto: R${valor_desconto:.2f} ({desconto:.2f}%)")
    txt_lines.append(f"Total final: R${total_final:.2f}")
    txt_lines.append("------------------------------------------")
    txt_lines.append("Obrigado e volte sempre!")

    txt_blob = "\n".join(txt_lines).encode("utf-8")

    # PDF (gera um PDF simples com fpdf)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, txt="CUPOM FISCAL", ln=True, align="C")
    pdf.ln(4)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, txt=f"Cliente: {nome}", ln=True)
    pdf.cell(0, 6, txt=f"Idade: {idade}    CPF: {cpf}    Pagamento: {pagamento}", ln=True)
    pdf.ln(4)
    for i in range(3):
        prod = data["Produto"][i] or "[--]"
        qtd = data["Qtd"][i]
        preco = data["Preço (R$)"][i]
        sub = data["Subtotal (R$)"][i]
        pdf.cell(0, 6, txt=f"{prod} | Qtd: {qtd} | Preço: R${preco:.2f} | Subtotal: R${sub:.2f}", ln=True)
    pdf.ln(4)
    pdf.cell(0, 6, txt=f"Total bruto: R${total_bruto:.2f}", ln=True)
    pdf.cell(0, 6, txt=f"Desconto: R${valor_desconto:.2f} ({desconto:.2f}%)", ln=True)
    pdf.cell(0, 6, txt=f"Total final: R${total_final:.2f}", ln=True)
    pdf_output = pdf.output(dest="S").encode("latin-1")  # bytes

    # ---------- Downloads ----------
    st.download_button("⬇️ Baixar cupom (CSV)", data=csv_bytes, file_name=f"{filename_base}.csv", mime="text/csv")
    st.download_button("⬇️ Baixar cupom (TXT)", data=txt_blob, file_name=f"{filename_base}.txt", mime="text/plain")
    st.download_button("⬇️ Baixar cupom (PDF)", data=pdf_output, file_name=f"{filename_base}.pdf", mime="application/pdf")

    st.success("Cupom gerado com sucesso! Você pode baixar em CSV, TXT ou PDF.")
    st.info("OBS: este app gera arquivos para download localmente. No Streamlit Cloud os arquivos não ficam armazenados permanentemente no servidor.")

    # ---------- Mostrar origem (se quiser link do seu arquivo original) ----------
    st.markdown("---")
    st.markdown(f"**Arquivo base usado:** `/mnt/data/App.py`")

