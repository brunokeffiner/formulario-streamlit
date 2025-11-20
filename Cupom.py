# Cupom.py - Cupom Fiscal Dinâmico (Versão Profissional)
import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF  # <-- IMPORT CORRETO
from datetime import datetime

st.set_page_config(page_title="Cupom Fiscal - Portfólio", page_icon="🏷️", layout="centered")

# ---------- Estilo ----------
st.markdown(
    """
    <style>
    .title { font-size:26px; font-weight:700; color:#0B3D91; margin-bottom:6px; }
    .subtitle { color:#444; margin-top:0px; margin-bottom:10px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>🏷️ Cupom Fiscal - Versão Profissional</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Adicione quantos produtos quiser — sistema dinâmico.</div>", unsafe_allow_html=True)
st.write("---")

# ---------- Inicializar lista de produtos ----------
if "produtos" not in st.session_state:
    st.session_state.produtos = []

# ---------- Dados do cliente ----------
with st.expander("Dados do Cliente", expanded=True):
    nome = st.text_input("Nome completo")
    idade = st.text_input("Idade")
    cpf = st.text_input("CPF")
    pagamento = st.selectbox("Forma de pagamento", ["Dinheiro", "Débito", "Crédito", "Pix", "Outro"])

# ---------- Adicionar produto ----------
st.markdown("### ➕ Adicionar produto")
with st.form("form_produto", clear_on_submit=True):
    p_nome = st.text_input("Nome do produto")
    p_preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
    p_qtd = st.number_input("Quantidade", min_value=1, step=1)
    adicionar = st.form_submit_button("Adicionar")

    if adicionar:
        subtotal = p_preco * p_qtd
        st.session_state.produtos.append({
            "Produto": p_nome or "[--]",
            "Qtd": int(p_qtd),
            "Preço (R$)": float(p_preco),
            "Subtotal (R$)": float(subtotal)
        })
        st.success(f"Produto '{p_nome}' adicionado!")

# ---------- Lista de produtos ----------
st.markdown("### 🧾 Itens adicionados")

if st.session_state.produtos:
    df = pd.DataFrame(st.session_state.produtos)
    st.table(df.style.format({"Preço (R$)": "{:.2f}", "Subtotal (R$)": "{:.2f}"}))

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Limpar todos os produtos"):
            st.session_state.produtos = []
            st.warning("Produtos removidos.")

    with col2:
        lista_remover = ["-"] + [f"{i+1} - {p['Produto']}" for i, p in enumerate(st.session_state.produtos)]
        rm_escolha = st.selectbox("Remover um item", lista_remover)
        if st.button("Remover selecionado") and rm_escolha != "-":
            idx = int(rm_escolha.split(" - ")[0]) - 1
            removido = st.session_state.produtos.pop(idx)
            st.success(f"Item removido: {removido['Produto']}")
else:
    st.info("Nenhum produto adicionado ainda.")

st.write("---")

# ---------- Desconto ----------
desconto = st.number_input("Desconto (%)", min_value=0.0, max_value=100.0, format="%.2f")

# ---------- Gerar cupom ----------
if st.button("🧾 Gerar cupom e arquivos"):

    if not st.session_state.produtos:
        st.error("Adicione produtos antes de gerar o cupom.")
    else:
        produtos = st.session_state.produtos
        total_bruto = sum([p["Subtotal (R$)"] for p in produtos])
        valor_desconto = total_bruto * (desconto / 100)
        total_final = total_bruto - valor_desconto

        # Mostrar cupom
        st.markdown("## 📄 Cupom Fiscal")
        st.write(f"**Cliente:** {nome}")
        st.write(f"**Idade:** {idade}  **CPF:** {cpf}")
        st.write(f"**Pagamento:** {pagamento}")

        df = pd.DataFrame(produtos)
        st.table(df.style.format({"Preço (R$)": "{:.2f}", "Subtotal (R$)": "{:.2f}"}))

        st.write("---")
        st.write(f"**Total bruto:** R$ {total_bruto:.2f}")
        st.write(f"**Desconto:** R$ {valor_desconto:.2f} ({desconto:.2f}%)")
        st.write(f"**Total final:** R$ {total_final:.2f}")
        st.write("---")

        # ---------- Arquivos ----------
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"cupom_{timestamp}"

        # CSV
        csv_buf = BytesIO()
        df.to_csv(csv_buf, index=False, float_format="%.2f")
        csv_bytes = csv_buf.getvalue()

        # TXT
        txt = []
        txt.append("-------------- CUPOM FISCAL --------------")
        txt.append(f"Cliente: {nome}")
        txt.append(f"Idade: {idade}    CPF: {cpf}    Pagamento: {pagamento}\n")
        for p in produtos:
            txt.append(f"{p['Produto']} | Qtd: {p['Qtd']} | Preço: R${p['Preço (R$)']:.2f} | Subtotal: R${p['Subtotal (R$)']:.2f}")
        txt.append("------------------------------------------")
        txt.append(f"Total bruto: R${total_bruto:.2f}")
        txt.append(f"Desconto: R${valor_desconto:.2f} ({desconto:.2f}%)")
        txt.append(f"Total final: R${total_final:.2f}")
        txt_blob = "\n".join(txt).encode("utf-8")

        # PDF (FPDF)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, "CUPOM FISCAL", ln=True, align="C")
        pdf.ln(3)

        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 6, f"Cliente: {nome}", ln=True)
        pdf.cell(0, 6, f"Idade: {idade}    CPF: {cpf}", ln=True)
        pdf.cell(0, 6, f"Pagamento: {pagamento}", ln=True)
        pdf.ln(4)

        for p in produtos:
            pdf.cell(0, 6, f"{p['Produto']} | Qtd: {p['Qtd']} | Preço: R${p['Preço (R$)']:.2f} | Subtotal: R${p['Subtotal (R$)']:.2f}", ln=True)

        pdf.ln(4)
        pdf.cell(0, 6, f"Total bruto: R${total_bruto:.2f}", ln=True)
        pdf.cell(0, 6, f"Desconto: R${valor_desconto:.2f}", ln=True)
        pdf.cell(0, 6, f"Total final: R${total_final:.2f}", ln=True)

        pdf_bytes = pdf.output(dest="S").encode("latin-1")

        # Download buttons
        st.download_button("📥 Baixar CSV", csv_bytes, f"{base}.csv")
        st.download_button("📥 Baixar TXT", txt_blob, f"{base}.txt")
        st.download_button("📥 Baixar PDF", pdf_bytes, f"{base}.pdf", mime="application/pdf")

        st.success("Cupom gerado com sucesso!")
