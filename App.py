import streamlit as st

st.title("Formulário de Cadastro")

A = st.text_input("Digite seu nome:")
B = st.text_input("Digite sua idade:")
C = st.text_input("Estado civil:")
d = st.text_input("Digite sua altura:")
e = st.text_input("Nacionalidade:")
g = st.text_input("Qual vaga você deseja?")
h = st.text_input("Qual sua pretensão salarial?")

if st.button("Enviar"):
    st.write(f"Olá, muito prazer em te conhecer, {A}!")
    st.write(f"Sua idade de {B} atende aos requisitos da nossa vaga.")
    st.write("É com imenso prazer que aceitamos a sua inscrição em nossa empresa! Seja bem-vinda!")
    st.write("Para continuar o seu cadastro precisamos que forneça mais algumas informações!")
    st.write(f"Você escolheu {g}.")
    st.write(f"Muito obrigada {A}, registramos seu interesse na vaga de {g} e sua pretensão salarial de {h}.")
    st.write("Em breve entraremos em contato com você para continuar o processo seletivo.")
