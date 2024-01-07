import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


# Firebase initialisatie
if not firebase_admin._apps:
        cred = credentials.Certificate("database-test-f1721-2a765cd61b0f.json")
        firebase_admin.initialize_app(cred)

def app():
    st.title("Fictief Data Dashboard - Powered By :blue[4DFinance]")

    # Initialisatie van sessiestatus variabelen
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'signedout' not in st.session_state:
        st.session_state['signedout'] = False

    def login_user(email, password):
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
        except:
            st.warning('Login Failed')

    def sign_out():
        st.session_state.signedout = False
        st.session_state.username = ''
        st.session_state.useremail = ''

    # Inlog/Registratie UI
    if not st.session_state.signedout:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            if st.button('Create my account'):
                user = auth.create_user(email=email, password=password, uid=username)
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()

        if choice == 'Login':
            if st.button('Login'):
                login_user(email, password)

    # Dashboard na inloggen
    elif st.session_state.signedout:
        def my_function(unique_id):
         if st.button('Sign out', key=f'unique_sign_out_button_{unique_id}'):
        
            theme_plotly = None


        df = pd.read_excel("Voorbeeld data Streamlit tool.xlsx", sheet_name="Data Ambulant")
        df = pd.read_excel("Voorbeeld data Streamlit tool.xlsx", sheet_name="Data GGZ") 
        df = pd.read_excel("Voorbeeld data Streamlit tool.xlsx", sheet_name="Data Verblijf")

        df_ambulant = pd.read_excel("Voorbeeld data Streamlit tool.xlsx", sheet_name="Data Ambulant")
        df_ggz = pd.read_excel("Voorbeeld data Streamlit tool.xlsx", sheet_name="Data GGZ") 
        df_verblijf = pd.read_excel("Voorbeeld data Streamlit tool.xlsx", sheet_name="Data Verblijf")


        tab1, tab2, tab3 = st.tabs(["Ambulant", "GGZ","Verblijf"])



        with tab1:
            st.header("Dashboard Ambulant")

            # Voeg een optie toe voor alle teams
            team_options = ['Alle Teams'] + list(df_ambulant['Team'].unique())
            selected_team_tab1 = st.selectbox('Selecteer een team', team_options, key='select_team_tab1_ambulant')


            # Controleer of 'Alle Teams' is geselecteerd
            if selected_team_tab1 == 'Alle Teams':
                filtered_df_ambulant = df_ambulant
            else:
                filtered_df_ambulant = df_ambulant[df_ambulant['Team'] == selected_team_tab1]

            # Dashboard Ambulant grafiek 1
            # Bereken de gemiddelden voor elke maand
            monthly_average = filtered_df_ambulant.groupby ('Maand').agg({
            'Productiviteit': 'mean',
            'Norm productiviteit': 'mean'
            }).reset_index()

            # Maak de lijngrafiek met Plotly Express
            fig = px.line(monthly_average, x='Maand', y=['Productiviteit', 'Norm productiviteit'],
                    labels={'value':'Percentage', 'variable':'Waarden'},
                    title='Gemiddelde Productiviteit vs. Norm Productiviteit per Maand')

            # Update de layout om percentages correct weer te geven
            # Assuming the percentages are already correct, we don't need to convert them again
            fig.update_traces(mode='lines+markers+text', texttemplate='%{y:.2f}%', textposition='top center')
            fig.update_layout(
            yaxis=dict(
                tickformat='.0%', 
                range=[0, 1]  
            ), 
            xaxis_title='Maand'
            )

            st.plotly_chart(fig, use_container_width=True)



            # Dashboard Ambulant grafiek 2
            monthly_data = filtered_df_ambulant.groupby('Maand').agg({
            'Productieve uren': 'sum',
            'Reisuren': 'sum',
            'Niet productieve uren': 'sum',
            'Uren feestdagen en vakantie': 'sum',
            'Ziekte uren': 'sum'
            }).reset_index()

            # Maak de gestapelde staafdiagram
            fig = go.Figure()

            # Voor elke categorie een staaf toevoegen
            categories = ['Productieve uren', 'Reisuren', 'Niet productieve uren', 'Uren feestdagen en vakantie', 'Ziekte uren']
            for category in categories:
                fig.add_trace(go.Bar(
                x=monthly_data['Maand'],
                y=monthly_data[category],
                name=category
            ))

            # Staafdiagram aanpassen om de staven te stapelen
            fig.update_layout(barmode='stack')

            # Labels en titels toevoegen
            fig.update_layout(
            title='Gestapelde Staafdiagram van Uren per Categorie per Maand',
            xaxis=dict(title='Maand'),
            yaxis=dict(title='Aantal Uren'),
            legend=dict(title='Waarden')
            )

            st.plotly_chart(fig, use_container_width=True)



            # Dashboard Ambulant grafiek 3
            # Bereken de gemiddelden voor elke maand
            monthly_sickness = filtered_df_ambulant.groupby('Maand').agg({
            'Ziekte': 'mean',
            'Norm Ziekte': 'mean'
            }).reset_index()

            # Maak de lijngrafiek met Plotly Express
            sickness_fig = px.line(monthly_sickness, x='Maand', y=['Ziekte', 'Norm Ziekte'],
                            labels={'value':'Percentage', 'variable':'Waarden'},
                            title='Gemiddelde Ziekte vs. Norm Ziekte per Maand')

            # Update de layout om percentages correct weer te geven en beperk de y-as
            sickness_fig.update_traces(mode='lines+markers+text', texttemplate='%{y:.2%}', textposition='top center')
            sickness_fig.update_layout(
            yaxis_tickformat='.0%',
            yaxis_range=[0, 0.1],
            xaxis_title='Maand'
            )

            st.plotly_chart(sickness_fig, use_container_width=True)



            # Dashboard Ambulant grafiek 4
            # Groepeer de data per 'Maand' en neem het gemiddelde van de 'Productiviteit bij aanwezigheid' en 'Norm Productiviteit bij aanwezigheid'
            monthly_productivity = filtered_df_ambulant.groupby('Maand').agg({
            'Productiviteit bij aanwezigheid': 'mean',
            'Norm Productiviteit bij aanwezigheid': 'mean'
            }).reset_index()

            # Maak het staafdiagram met Plotly Express
            fig = px.bar(
            monthly_productivity, 
            x='Maand', 
            y='Productiviteit bij aanwezigheid',
            barmode='group',
            labels={'value':'Percentage', 'variable':'Waarden'},
            title='Productiviteit vs. Norm Productiviteit bij Aanwezigheid per Maand'
            )

            # Voeg een lijndiagram toe voor 'Norm Productiviteit bij aanwezigheid'
            fig.add_trace(
            go.Scatter(
                x=monthly_productivity['Maand'], 
                y=monthly_productivity['Norm Productiviteit bij aanwezigheid'],
                mode='lines+markers',
                name='Norm Productiviteit bij aanwezigheid'
            )
            )

        
            fig.update_layout(
            yaxis_tickformat='.0%',
            yaxis_range=[0, 1],
            xaxis_title='Maand'
            )


            st.plotly_chart(fig, use_container_width=True)


        with tab2:
            st.header("Dashboard GGZ")


            # Voeg een optie toe voor alle teams
            team_options_ggz = ['Alle Teams'] + list(df_ggz['Team'].unique())
            selected_team_tab2 = st.selectbox('Selecteer een ander team', team_options_ggz, key='select_team_tab2_ggz')


            # Controleer of 'Alle Teams' is geselecteerd
            if selected_team_tab2 == 'Alle Teams':
                filtered_df_ggz = df_ggz
            else:
                filtered_df_ggz = df_ggz[df_ggz['Team'] == selected_team_tab2]



            # Dashboard GGZ grafiek 1
            # Bereken de gemiddelden voor elke maand
            monthly_average = filtered_df_ggz.groupby('Maand').agg({
            'Productiviteit': 'mean',
            'Norm productiviteit': 'mean'
            }).reset_index()

            # Maak de lijngrafiek met Plotly Express
            fig = px.line(monthly_average, x='Maand', y=['Productiviteit', 'Norm productiviteit'],
                    labels={'value':'Percentage', 'variable':'Waarden'},
                    title='Gemiddelde Productiviteit vs. Norm Productiviteit per Maand')

            # Update de layout om percentages correct weer te geven
            # Assuming the percentages are already correct, we don't need to convert them again
            fig.update_traces(mode='lines+markers+text', texttemplate='%{y:.2f}%', textposition='top center')
            fig.update_layout(
            yaxis=dict(
                tickformat='.0%', 
                range=[0, 1]  # Adjust the y-axis to show from 0% to 100%
            ), 
            xaxis_title='Maand'
            )

            st.plotly_chart(fig, use_container_width=True)



            # Dashboard GGZ grafiek 2

            monthly_data = filtered_df_ggz.groupby('Maand').agg({
            'Productieve uren': 'sum',
            'Niet productieve uren': 'sum',
            'Uren feestdagen en vakantie': 'sum',
            'Ziekte uren': 'sum'
            }).reset_index()

            # Maak de gestapelde staafdiagram
            fig = go.Figure()

            # Voor elke categorie een staaf toevoegen
            categories = ['Productieve uren', 'Niet productieve uren', 'Uren feestdagen en vakantie', 'Ziekte uren']
            for category in categories:
                fig.add_trace(go.Bar(
                x=monthly_data['Maand'],
                y=monthly_data[category],
                name=category
            ))

            # Staafdiagram aanpassen om de staven te stapelen
            fig.update_layout(barmode='stack')

            # Labels en titels toevoegen
            fig.update_layout(
            title='Gestapelde Staafdiagram van Uren per Categorie per Maand',
            xaxis=dict(title='Maand'),
            yaxis=dict(title='Aantal Uren'),
            legend=dict(title='Waarden')
            )

            st.plotly_chart(fig, use_container_width=True)



            # Dashboard GGZ grafiek 3
            # Bereken de gemiddelden voor elke maand
            monthly_sickness = filtered_df_ggz.groupby('Maand').agg({
            'Ziekte': 'mean',
            'Norm Ziekte': 'mean'
            }).reset_index()

            # Maak de lijngrafiek met Plotly Express
            sickness_fig = px.line(monthly_sickness, x='Maand', y=['Ziekte', 'Norm Ziekte'],
                            labels={'value':'Percentage', 'variable':'Waarden'},
                            title='Gemiddelde Ziekte vs. Norm Ziekte per Maand')

            # Update de layout om percentages correct weer te geven en beperk de y-as
            sickness_fig.update_traces(mode='lines+markers+text', texttemplate='%{y:.2%}', textposition='top center')
            sickness_fig.update_layout(
            yaxis_tickformat='.0%',
            yaxis_range=[0, 0.1],
            xaxis_title='Maand'
            )

            st.plotly_chart(sickness_fig, use_container_width=True)



            # Dashboard GGZ grafiek 4
            # Groepeer de data per 'Maand' en neem het gemiddelde van de 'Productiviteit bij aanwezigheid' en 'Norm Productiviteit bij aanwezigheid'
            monthly_productivity = filtered_df_ggz.groupby('Maand').agg({
            'Productiviteit bij aanwezigheid': 'mean',
            'Norm Productiviteit bij aanwezigheid': 'mean'
            }).reset_index()

            # Maak het staafdiagram met Plotly Express
            fig = px.bar(
            monthly_productivity, 
            x='Maand', 
            y='Productiviteit bij aanwezigheid',
            barmode='group',
            labels={'value':'Percentage', 'variable':'Waarden'},
            title='Productiviteit vs. Norm Productiviteit bij Aanwezigheid per Maand'
            )

            # Voeg een lijndiagram toe voor 'Norm Productiviteit bij aanwezigheid'
            fig.add_trace(
            go.Scatter(
                x=monthly_productivity['Maand'], 
                y=monthly_productivity['Norm Productiviteit bij aanwezigheid'],
                mode='lines+markers',
                name='Norm Productiviteit bij aanwezigheid'
            )
            )

        
            fig.update_layout(
            yaxis_tickformat='.0%',
            yaxis_range=[0, 1],
            xaxis_title='Maand'
            )


            st.plotly_chart(fig, use_container_width=True)


        with tab3:
            st.header("Dashboard Verblijf")

        
            # Voeg een optie toe voor alle locaties
            locatie_options_verblijf = ['Alle Locaties'] + list(df_verblijf['Locatie'].unique())
            selected_locatie_verblijf = st.selectbox('Selecteer een locatie voor Verblijf', locatie_options_verblijf, key='select_locatie_verblijf')

            # Controleer of 'Alle Locaties' is geselecteerd
            if selected_locatie_verblijf == 'Alle Locaties':
                filtered_df_verblijf = df_verblijf
            else:
                filtered_df_verblijf = df_verblijf[df_verblijf['Locatie'] == selected_locatie_verblijf]




            # Dashboard Verblijf grafiek 1
            # Bereken de sommen voor elke maand
            monthly_aggregate = filtered_df_verblijf.groupby('Maand').agg({
                'Normuren': 'sum',
                'Aantal bewoners': 'sum'
            }).reset_index()


            bar_trace = go.Bar(
                x=monthly_aggregate['Maand'],
                y=monthly_aggregate['Aantal bewoners'],
                name='Som van Aantal bewoners',
                marker=dict(color='grey', opacity=0.7), 
                yaxis='y2'  
            )

         
            line_trace = go.Scatter(
                x=monthly_aggregate['Maand'],
                y=monthly_aggregate['Normuren'],
                name='Som van Normuren',
                mode='lines+markers',
                line=dict(color='orange', width=2)
            )


            layout = go.Layout(
                title='Som van Aantal bewoners vs Som van Normuren per Maand',
                xaxis=dict(title='Maand'),
                yaxis=dict(
                    title='Som van Normuren',  
                    side='left',  
                    showgrid=False,  
                ),
                yaxis2=dict(
                    title='Som van Aantal bewoners',  
                    overlaying='y',  
                    side='right',  
                    showgrid=False,  
                ),
                margin=dict(l=40, r=40, t=40, b=40),
                legend=dict(x=0.1, y=1.1, orientation="h"),
            )

    
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            
            fig.update_layout(
                barmode='group',
                template='plotly_white',
                legend_title_text='Waarden'
            )

           
            fig['layout']['yaxis'].update(range=[3200, 4000], autorange=False)
            fig['layout']['yaxis2'].update(range=[49, 54], autorange=False)

          
            st.plotly_chart(fig, use_container_width=True)



            # Dashboard Verblijf grafiek 2

            # Group the data by 'Maand'
            monthly_aggregate = filtered_df_verblijf.groupby('Maand').agg({
                'Geroosterde uren': 'sum',
                'Normuren': 'sum'
            }).reset_index()

            # Create the bar chart for 'Geroosterde uren'
            bar_trace = go.Bar(
                x=monthly_aggregate['Maand'],
                y=monthly_aggregate['Geroosterde uren'],
                name='Som van Geroosterde uren',
                marker=dict(color='orange')
            )

            # Create the line chart for 'Normuren'
            line_trace = go.Scatter(
                x=monthly_aggregate['Maand'],
                y=monthly_aggregate['Normuren'],
                name='Som van Normuren',
                mode='lines+markers',
                line=dict(color='blue'),
                )

            # Define the layout with dual y-axes
            layout = go.Layout(
                title='Som van Geroosterde uren vs Som van Normuren per Maand',
                xaxis=dict(title='Maand'),
                yaxis=dict(title='Som van Geroosterde uren'),
                legend=dict(x=0.1, y=1.1, orientation="h")
            )

            
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            
            fig.update_layout(
                yaxis=dict(range=[3100, 4000]),
            )

            
            st.plotly_chart(fig, use_container_width=True)



            # Dashboard Verblijf grafiek 3
            # Group the data by 'Maand' and 'Functie'
            grouped = filtered_df_verblijf.groupby(['Maand', 'Functie'])['Geroosterde uren'].sum().reset_index()

            # Pivot the grouped data to get 'Functie' as columns
            pivot = grouped.pivot(index='Maand', columns='Functie', values='Geroosterde uren').fillna(0)

            # Create traces for each 'Functie'
            traces = []
            for functie in pivot.columns:
                traces.append(go.Bar(
                    x=pivot.index,
                    y=pivot[functie],
                    name=functie
                ))

            # Define the layout for the stacked bar chart
            layout = go.Layout(
                title='Som van Geroosterde uren per Maand en Functie',
                xaxis=dict(title='Maand'),
                yaxis=dict(title='Som van Geroosterde uren'),
                barmode='stack'
            )

            
            fig = go.Figure(data=traces, layout=layout)

            
            st.plotly_chart(fig, use_container_width=True)