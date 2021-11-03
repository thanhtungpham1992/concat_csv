import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import chardet
import io

st.title('Concatenate file and detect decode')
st.write('## Nối các file csv cùng định dạng')
menu = ["Concatenate File", "Detect decode"]
choice = st.sidebar.selectbox('Menu',menu)

if choice == 'Concatenate File':
    with st.form(key='my_form_1'):
        lst_files = st.file_uploader("Upload CSV files", accept_multiple_files=True, type=(['csv']))
        decode = st.radio('Bảng mã decode', options=['utf8', 'iso-8859-1', 'ascii','cp1252', 'Auto detect'])
        file_type = st.radio('File type export', options=['*.csv','*.xlsx'])
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.write('### Total file, encoding:')
        # for i in lst_files:
        #     if i is not None:
        #         st.write(i.name)
        #     else:
        #         None

        data = pd.DataFrame()
        for i in lst_files:
            if decode == 'Auto detect':
                encode = chardet.detect(i.read())['encoding']
                i.seek(0)
            else:
                encode = decode
            st.write(i.name,encode)
            temp = pd.read_csv(i,encoding=encode,index_col=False)
            temp['File'] = i.name
            data = pd.concat([data,temp])
        st.write('### Data concatenated:')
        st.dataframe(data)
        dt_string = datetime.now().strftime("%d%m%Y_%H%M%S")
        if file_type == '*.csv':
            st.download_button(data=data.to_csv(index=False, encoding='UTF-8'), label='Download CSV File', file_name='concat_file_'+dt_string+'.csv')
        elif file_type == '*.xlsx':
            buffer = io.BytesIO()
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # Write each dataframe to a different worksheet.
                data.to_excel(writer, sheet_name='concat_file', index=False, )
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.save()
                st.download_button(label="Download Excel File", data=buffer, file_name='concat_file_'+dt_string+'.xlsx')
elif choice == 'Detect decode':
    with st.form(key='my_form_2'):
        lst_files = st.file_uploader('Upload CSV files', accept_multiple_files=True, type=(['csv']))
        # for i in lst_files:
        #     if i is not None:
        #         st.write(i.name)
        #     else:
        #         None
        submit_button = st.form_submit_button(label='Submit')
    for i in lst_files:
        # look at the first ten thousand bytes to guess the character encoding
        rawdata = i.read()
        result = chardet.detect(rawdata)
        st.write(i.name,result['encoding'],result['confidence'])