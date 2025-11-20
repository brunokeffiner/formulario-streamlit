# Cupom.py - Cupom Fiscal Dinâmico (Versão Profissional - Portfólio)
import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf2 import FPDF
from datetime import datetime

st.set_page_config(page_title="Cupom Fiscal - Portfólio", page_icon="🏷️", layout="centered")

# ---------- Estilo simples ----------
st.markdown(
    """
    <style>
    .title { font-size:26px; font-weight:700; color:#0B3D91; margin-bottom:6px; }
    .subtitle { color:#444; margin-top:0px; margin-bottom:10px; }
    .box { padding:12px; border-radius:8px; background:#fff; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>🏷️ Cupom Fiscal - Versão Profissional</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Interface limpa para portfólio — adicione quantos produtos quiser.</div>", unsafe_allow_html=True)
st.write("---")

# ---------- Inicializar session_state ----------
if "produtos" not in st.session_state:
    st.session_state.produtos = []  # cada item: dict {nome, preco, qtd, subtotal}

# ---------- Dados do cliente ----------
with st.expander("Dados do Cliente", expanded=True):
    col1, col2 = st.columns([3,1])
    with col1:
        nome = st.text_input("Nome completo", key="cli_nome")
        cpf = st.text_input("CPF", key="cli_cpf")
    with col2:
        idade = st.text_input("Idade", key="cli_idade")
        pagamento = st.selectbox("Forma de pagamento", ["Dinheiro", "Débito", "Crédito", "Pix", "Outro"], key="cli_pag")

st.write("")

# ---------- Formulário para adicionar produto ----------
st.markdown("### ➕ Adicionar produto")
with st.form(key="produto_form", clear_on_submit=True):
    p_name = st.text_input("Nome do produto", key="form_nome")
    p_price = st.number_input("Preço (R$)", min_value=0.0, format="%.2f", key="form_preco")
    p_qtd = st.number_input("Quantidade", min_value=1, step=1, key="form_qtd")
    add = st.form_submit_button("Adicionar produto")
    if add:
        subtotal = float(p_price) * int(p_qtd)
        st.session_state.produtos.append({
            "Produto": p_name or "[--]",
            "Qtd": int(p_qtd),
            "Preço (R$)": float(p_price),
            "Subtotal (R$)": float(subtotal)
        })
        st.success(f"Produto '{p_name}' adicionado (Qtd {p_qtd})")

st.write("")

# ---------- Lista de produtos adicionados e ações ----------
st.markdown("### 🧾 Itens adicionados")
if st.session_state.produtos:
    df = pd.DataFrame(st.session_state.produtos)
    st.table(df.style.format({"Preço (R$)": "{:.2f}", "Subtotal (R$)": "{:.2f}"}))

    colA, colB = st.columns([1,1])
    with colA:
        limpar = st.button("🗑️ Limpar itens")
    with colB:
        remover = st.selectbox("Remover item (pelo índice)", ["-"] + [f"{i+1} - {it['Produto']}" for i,it in enumerate(st.session_state.produtos)])
        rm_btn = st.button("Remover selecionado")

    if limpar:
        st.session_state.produtos = []
        st.success("Lista de produtos limpa.")
    if rm_btn and remover != "-":
        idx = int(remover.split(" - ")[0]) - 1
        nome_removido = st.session_state.produtos[idx]["Produto"]
        st.session_state.produtos.pop(idx)
        st.success(f"Removido: {nome_removido}")
else:
    st.info("Nenhum produto adicionado ainda. Use o formulário acima para incluir itens.")

st.write("---")

# ---------- Desconto e geração ----------
desconto = st.number_input("Desconto (%)", min_value=0.0, max_value=100.0, format="%.2f", value=0.0)
gerar = st.button("🧾 Gerar cupom e arquivos")

if gerar:
    produtos = st.session_state.produtos
    if not produtos:
        st.error("Adicione pelo menos um produto antes de gerar o cupom.")
    else:
        # cálculos
        subtotal_values = [p["Subtotal (R$)"] for p in produtos]
        total_bruto = sum(subtotal_values)
        valor_desconto = total_bruto * (desconto / 100.0)
        total_final = total_bruto - valor_desconto

        # Exibir cupom na tela
        st.markdown("## 📄 Cupom Fiscal")
        st.markdown(f"**Cliente:** {nome or '[não informado]'}")
        st.markdown(f"**Idade:** {idade}  **CPF:** {cpf}  **Pagamento:** {pagamento}")

        df = pd.DataFrame(produtos)
        st.table(df.style.format({"Preço (R$)": "{:.2f}", "Subtotal (R$)": "{:.2f}"}))

        st.markdown("---")
        st.write(f"**Total bruto:** R$ {total_bruto:.2f}")
        st.write(f"**Desconto:** {desconto:.2f}% (R$ {valor_desconto:.2f})")
        st.write(f"**Total final:** R$ {total_final:.2f}")
        st.markdown("---")

        # preparar downloads
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"cupom_{timestamp}"

        # CSV
        csv_buf = BytesIO()
        pd.DataFrame(produtos).to_csv(csv_buf, index=False, float_format="%.2f")
        csv_bytes = csv_buf.getvalue()

        # TXT (formatado)
        txt_lines = []
        txt_lines.append("-------------- CUPOM FISCAL --------------")
        txt_lines.append(f"Cliente: {nome or '[--]'}")
        txt_lines.append(f"Idade: {idade}    CPF: {cpf}    Pagamento: {pagamento}")
        txt_lines.append("")
        for p in produtos:
            txt_lines.append(f"{p['Produto']}  |  Qtd: {p['Qtd']}  |  Preço: R${p['Preço (R$)']:.2f}  |  Subtotal: R${p['Subtotal (R$)']:.2f}")
        txt_lines.append("------------------------------------------")
        txt_lines.append(f"Total bruto: R${total_bruto:.2f}")
        txt_lines.append(f"Desconto: R${valor_desconto:.2f} ({desconto:.2f}%)")
        txt_lines.append(f"Total final: R${total_final:.2f}")
        txt_lines.append("------------------------------------------")
        txt_lines.append("Obrigado e volte sempre!")
        txt_blob = "\n".join(txt_lines).encode("utf-8")

        # PDF com fpdf2
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, "CUPOM FISCAL", ln=True, align="C")
        pdf.ln(4)
        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 6, f"Cliente: {nome or '[--]'}", ln=True)
        pdf.cell(0, 6, f"Idade: {idade}    CPF: {cpf}", ln=True)
        pdf.cell(0, 6, f"Pagamento: {pagamento}", ln=True)
        pdf.ln(4)
        for p in produtos:
            pdf.cell(0, 6, f"{p['Produto']} | Qtd: {p['Qtd']} | Preço: R${p['Preço (R$)']:.2f} | Subtotal: R${p['Subtotal (R$)']:.2f}", ln=True)
        pdf.ln(4)
        pdf.cell(0, 6, f"Total bruto: R${total_bruto:.2f}", ln=True)
        pdf.cell(0, 6, f"Desconto: R${valor_desconto:.2f} ({desconto:.2f}%)", ln=True)
        pdf.cell(0, 6, f"Total final: R${total_final:.2f}", ln=True)
        pdf_bytes = pdf.output(dest="S").encode("latin-1")

        # downloads
        st.download_button("📥 Baixar CSV", csv_bytes, file_name=f"{base}.csv", mime="text/csv")
        st.download_button("📥 Baixar TXT", txt_blob, file_name=f"{base}.txt", mime="text/plain")
        st.download_button("📥 Baixar PDF", pdf_bytes, file_name=f"{base}.pdf", mime="application/pdf")

        st.success("Cupom gerado com sucesso! (Arquivos prontos para download)")

st.markdown("---")
st.markdown("**Base:** code adapted from `/mnt/data/App.py`")
