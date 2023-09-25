import streamlit as st

'''def main():
    # Exibindo o logotipo no sidebar
    logo_image = '/Users/reinaldoblack/Downloads/logo/logo.png'
    st.sidebar.image(logo_image, use_column_width=True)

if __name__ == '__main__':
    main()
'''

'''# Exibindo o logotipo no sidebar
logo_image = '/Users/reinaldoblack/Downloads/logo/logo.png'
st.sidebar.image(logo_image, use_column_width=True)
import streamlit as st
'''

# Definindo as opções do menu
opcoes_menu = ["Página Inicial", "Temperatura", "Outras Páginas"]
pagina_selecionada = st.sidebar.radio("Navegar", opcoes_menu)

# Lógica para exibir conteúdo com base na página selecionada
if pagina_selecionada == "Página Inicial":
    # Conteúdo da página inicial
    st.title("Bem-vindo à Página Inicial!")
    # ...

elif pagina_selecionada == "Temperatura":
    # Submenu para Temperatura
    submenu_temperatura = ["Página de Temperatura", "Outra Página de Temperatura"]
    subpagina_selecionada = st.sidebar.radio("Temperatura", submenu_temperatura)

    if subpagina_selecionada == "Página de Temperatura":
        # Conteúdo da página de temperatura
        st.title("Página de Temperatura")
        # ...

    elif subpagina_selecionada == "Outra Página de Temperatura":
        # Conteúdo de outra página de temperatura
        st.title("Outra Página de Temperatura")
        # ...

elif pagina_selecionada == "Outras Páginas":
    # Conteúdo de outras páginas
    st.title("Outras Páginas")
    # ...