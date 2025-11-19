import streamlit as st

# ======== ESTILO DA PÁGINA ========
st.set_page_config(
    page_title="UNOPAR Vila Velha - Cadastro",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
    <h1 style='text-align: center; color: #1E90FF;'>
        🎓 UNOPAR Vila Velha
    </h1>
    <h3 style='text-align: center; color: #333;'>
        O lugar onde os seus sonhos podem se tornar realidade!
    </h3>
    <hr>
""", unsafe_allow_html=True)

# ======== APRESENTAÇÃO ========
st.write("Olá, seja bem-vindo(a) à **UNOPAR Vila Velha**!")
st.write("Antes de começarmos, precisamos saber um pouco sobre você.")

matricula = st.selectbox(
    "Você gostaria de se matricular na melhor rede de ensino do Espírito Santo?",
    ["Sim", "Não"]
)

if matricula == "Não":
    st.warning("Tudo bem! Quando estiver pronta(o), estaremos aqui para te receber! 😊")
else:
    st.success("Ótimo! Nossa equipe está pronta para te levar ao caminho do sucesso.")

    # ======== CADASTRO ========
    st.markdown("### 📘 Escolha a área que deseja cursar:")
    area = st.selectbox(
        "Qual área deseja cursar?",
        ["Enfermagem", "Direito", "Administração", "Educação Física", "Análise e Desenvolvimento de Sistemas", "Psicologia", "Pedagogia", "Outro"]
    )

    st.info(f"Você escolheu: **{area}**. Agora vamos concluir seu cadastro!")

    st.markdown("### 📝 Dados Pessoais")

    nome = st.text_input("Nome completo")
    idade = st.number_input("Idade", min_value=1, max_value=120, step=1)
    estado_civil = st.selectbox(
        "Estado civil",
        ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"]
    )
    nacionalidade = st.text_input("Nacionalidade")
    ensino = st.selectbox("Possui ensino médio completo?", ["Sim", "Não"])
    contato = st.text_input("Contato (telefone)")

    # ======== BOTÃO FINAL ========
    if st.button("Concluir Cadastro"):
        if nome and contato:
            st.success(f"Muito prazer, {nome}! Seu cadastro foi realizado com sucesso! 🎉")
            st.write(f"Em breve entraremos em contato pelo número **{contato}** para iniciarmos o processo de alocação de turmas.")
            st.markdown("""
                <p style='text-align: center; margin-top: 20px; font-size: 18px; color: #1E90FF;'>
                    Sinta-se segura em contar conosco!  
                    <br>Seu futuro é a nossa alegria!  
                    <br><b>UNOPAR Vila Velha 💙</b>
                </p>
            """, unsafe_allow_html=True)
        else:
            st.error("Por favor, preencha **pelo menos o nome e o telefone** para concluir o cadastro.")
