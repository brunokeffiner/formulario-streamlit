import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf2 import FPDF   # <- fpdf2 (correto para Streamlit Cloud)
from datetime import datetime

st.set_page_config(page_title="Cupom Fiscal", page_icon="🧾")

st.title("🧾 Cupom Fiscal - Versão Profissional")
st.write("Adicione produtos, gere cupom e faça download em PDF, TXT ou CSV.")

# -------------------- Sessão de produtos --------------------
if "produtos" not in st.session_state:
    st.session_state.produtos = []

# -------------------- Dados do Cliente --------------------
st.header("📌 Dados do Cliente")
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome completo")
    idade = st.text_input("Idade")
with col2:
    cpf = st.text_input("CPF")
    pagamento = st.selectbox("Forma de pagamento", ["Pix", "Débito", "Crédito", "Dinheiro"])

st.write("---")

# -------------------- Adicionar Produto --------------------
st.header("➕ Adicionar Produto")

with st.form("form_produto", clear_on_submit=True):
    p_nome = st.text_input("Nome do produto")
    p_preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
    p_qtd = st.number_input("Quantidade", min_value=1, step=1)

    adicionar = st.form_submit_button("Adicionar produto")

    if adicionar:
        subtotal = p_preco * p_qtd
        st.session_state.produtos.append({
            "Produto": p_nome,
            "Qtd": int(p_qtd),
            "Preço (R$)": float(p_preco),
            "Subtotal (R$)": float(subtotal)
        })
        st.success(f"Produto '{p_nome}' adicionado!")

st.write("---")

# -------------------- Lista de Produtos --------------------
st.header("🛒 Produtos adicionados")

if st.session_state.produtos:
    df = pd.DataFrame(st.session_state.produtos)
    st.table(df.style.format({"Preço (R$)": "{:.2f}", "Subtotal (R$)": "{:.2f}"}))

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Limpar todos os produtos"):
            st.session_state.produtos = []
            st.warning("Produtos removidos.")

    with col2:
        lista = ["-"] + [f"{i+1} - {p['Produto']}" for i, p in enumerate(st.session_state.produtos)]
        rm = st.selectbox("Remover item", lista)
        if st.button("Remover selecionado") and rm != "-":
            idx = int(rm.split(" - ")[0]) - 1
            removido = st.session_state.produtos.pop(idx)
            st.success(f"Item removido: {removido['Produto']}")

else:
    st.info("Nenhum produto adicionado.")

st.write("---")

# -------------------- Desconto --------------------
desconto = st.number_input("Desconto (%)", min_value=0.0, max_value=100.0, format="%.2f")

# -------------------- Gerar Cupom --------------------
if st.button("📄 Gerar cupom e arquivos"):

    if not st.session_state.produtos:
        st.error("Adicione produtos antes de gerar o cupom.")
    else:
        produtos = st.session_state.produtos

        total_bruto = sum([p["Subtotal (R$)"] for p in produtos])
        valor_desc = total_bruto * (desconto / 100)
        total_final = total_bruto - valor_desc

        # ---------- Exibir Cupom ----------
        st.subheader("📄 Cupom Fiscal")
        st.write(f"**Cliente:** {nome}")
        st.write(f"**CPF:** {cpf} — **Idade:** {idade}")
        st.write(f"**Pagamento:** {pagamento}")

        st.table(df.style.format({"Preço (R$)": "{:.2f}", "Subtotal (R$)": "{:.2f}"}))

        st.write(f"**Total bruto:** R$ {total_bruto:.2f}")
        st.write(f"**Desconto:** R$ {valor_desc:.2f} ({desconto:.1f}%)")
        st.write(f"### Total final: R$ {total_final:.2f}")

        # ---------------- TXT ----------------
        txt = []
        txt.append("----------- CUPOM FISCAL -----------")
        txt.append(f"Cliente: {nome}")
        txt.append(f"CPF: {cpf}  |  Idade: {idade}")
        txt.append(f"Pagamento: {pagamento}\n")

        for p in produtos:
            txt.append(f"{p['Produto']} | Qtd: {p['Qtd']} | Preço: R${p['Preço (R$)']:.2f} | Subtotal: R${p['Subtotal (R$)']:.2f}")

        txt.append("------------------------------------")
        txt.append(f"Total bruto: R${total_bruto:.2f}")
        txt.append(f"Desconto: R${valor_desc:.2f}")
        txt.append(f"Total final: R${total_final:.2f}")

        txt_bytes = "\n".join(txt).encode("utf-8")

        # ---------------- CSV ----------------
        csv_buf = BytesIO()
        df.to_csv(csv_buf, index=False)
        csv_bytes = csv_buf.getvalue()

        # ---------------- PDF (FPDF2 — SEM ERRO) ----------------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 10, "CUPOM FISCAL", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.set_font("Helvetica", size=10)

        pdf.cell(0, 6, f"Cliente: {nome}", ln=True)
        pdf.cell(0, 6, f"CPF: {cpf}  |  Idade: {idade}", ln=True)
        pdf.cell(0, 6, f"Pagamento: {pagamento}", ln=True)
        pdf.ln(4)

        for p in produtos:
            pdf.cell(0, 6, f"{p['Produto']}  |  Qtd: {p['Qtd']}  |  Preço: R${p['Preço (R$)']:.2f}  |  Subtotal: R${p['Subtotal (R$)']:.2f}", ln=True)

        pdf.ln(4)
        pdf.cell(0, 6, f"Total bruto: R${total_bruto:.2f}", ln=True)
        pdf.cell(0, 6, f"Desconto: R${valor_desc:.2f}", ln=True)
        pdf.cell(0, 6, f"Total final: R${total_final:.2f}", ln=True)

        # ---------- AQUI ESTÁ A CORREÇÃO: fpdf2 retorna bytes nativos ----------
        pdf_bytes = pdf.output(dest="S")
        # ----------------------------------------------------------------------

        # ---------------- Botões de Download ----------------
        st.download_button("📥 Baixar TXT", txt_bytes, "cupom.txt")
        st.download_button("📥 Baixar CSV", csv_bytes, "cupom.csv")
        st.download_button("📥 Baixar PDF", pdf_bytes, "cupom.pdf", mime="application/pdf")

        st.success("Cupom gerado com sucesso!")
