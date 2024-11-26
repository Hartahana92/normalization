import pandas as pd
import streamlit as st
import logging

logging.basicConfig(filename='app_errors.log', level=logging.ERROR)

st.title("Нормализация метаболитов")

uploaded_file_norm = st.file_uploader("Загрузите файл с данными", type=["xlsx"])
uploaded_file_ref = st.file_uploader("Загрузите файл с референсными данными", type=["xlsx"])
    # Чтение загруженных файлов
if uploaded_file_norm and uploaded_file_ref:
    # Чтение загруженных файлов
    data_norm = pd.read_excel(uploaded_file_norm)
    data_LabQC = data_norm[data_norm['Group'] == 'LabQC']
    data_ref = pd.read_excel(uploaded_file_ref, sheet_name='Reference')

    metabolites = ['5-hydroxytryptophan', 'Adenosin', 'ADMA', 'Alanine',
                   'Antranillic acid', 'Arginine', 'Asparagine', 'Aspartic acid',
                   'Betaine', 'Carnosine', 'Choline', 'Citrulline', 'Cortisol',
                   'Creatinine', 'Cytidine', 'DMG', 'Glutamic acid', 'Glutamine',
                   'Glycine', 'HIAA', 'Histamine', 'Histidine', 'Homoarginine',
                   'Hydroxyproline', 'Indole-3-acetic acid', 'Indole-3-butyric',
                   'Indole-3-carboxaldehyde', 'Indole-3-lactic acid',
                   'Indole-3-propionic acid', 'Kynurenic acid', 'Kynurenine', 'Lysine',
                   'Melatonin', 'Methionine', 'Methionine-Sulfoxide', 'Methylhistidine',
                   'Ornitine', 'Pantothenic', 'Phenylalanine', 'Proline',
                   'Quinolinic acid', 'Riboflavin', 'Serine', 'Serotonin', 'Summ Leu-Ile',
                   'Taurine', 'Threonine', 'TMAO', 'TotalDMA (SDMA)', 'Tryptamine', 'Tryptophan', 'Tyrosin', 'Uridine', 'Valine', 'Xanthurenic acid', 'C0',
                   'C10', 'C10-1', 'C10-2', 'C12', 'C12-1', 'C14', 'C14-1', 'C14-2',
                   'C14-OH', 'C16', 'C16-1', 'C16-1-OH', 'C16-OH', 'C18', 'C18-1',
                   'C18-1-OH', 'C18-2', 'C18-OH', 'C2', 'C3', 'C4', 'C5', 'C5-1', 'C5-DC',
                   'C5-OH', 'C6', 'C6-DC', 'C8', 'C8-1']

    # Нормализация данных
    coefs_batch = []
    for column in metabolites:
        mean_ref = data_ref[column].loc[0]
        coef_batch = mean_ref / data_LabQC[column].median()
        coefs_batch.append(coef_batch)
    coefs = pd.DataFrame({'Metabolite': metabolites, 'Batch_1': coefs_batch})

        # Применение коэффициентов к данным
    for i, metabolite in enumerate(metabolites):
        coef_n = coefs[coefs['Metabolite'] == metabolite]
        data_norm[metabolite] = data_norm[metabolite] * coef_n['Batch_1'].values[0]

    output_buffer = pd.ExcelWriter('Kopylov_b5_normalized.xlsx', engine='xlsxwriter')
    data_norm.to_excel(output_buffer, index=False)
    output_buffer.close() 

 #Сообщение об успешном завершении
    st.success("Нормализация завершена!")

# Отображение нормализованных данных
    st.subheader("Нормализованные данные")
    st.dataframe(data_norm)

# Кнопка для скачивания нормализованных данных
    with open('Kopylov_b5_normalized.xlsx', 'rb') as f:
        st.download_button(
            label="Скачать нормализованные данные",
            data=f,
            file_name='Kopylov_b5_normalized.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    
    
    
####################    
