import streamlit as st
import os, csv
import pandas as pd
import numpy as np


st.title('Nối File CSV')
st.write('## Thực hiện nối các file csv cùng định dạng')
with st.form(key='my_form'):
    path = st.text_input('Nhập đường dẫn tới folder chưa file chỉ chứa CSV')
    path_op = st.text_input('Nhập đường dẫn lưu file nối (Để trống file sẽ lưu ở Folder gốc)')
    st.text('Example: C:\Folder\Folder\Folder\...\Folder_csv')
    decode = st.radio('Bảng mã decode', options=['utf8', 'iso-8859-1', 'utf16', 'utf32'])
    submit_button = st.form_submit_button(label='Submit')

if submit_button and path != '':
    files = os.listdir(path)
    for i in files:
        if i.lower().find('.csv') == -1:
            files.remove(i)
    st.write('## File CSV in folder:')
    st.text(pd.DataFrame(files, columns=['CSV file']))

    shop = pd.read_csv(path + '\\' + files[0],encoding=decode,index_col=False)   
    shop['File'] = files[0]
    for i in range(1,len(files)):
        temp = pd.read_csv(path + '\\' + files[i],encoding=decode,index_col=False)
        temp['File'] = files[i]
        shop = pd.concat([shop,temp])
    st.write('## Data:')
    st.dataframe(shop)

    if path_op == '':
        shop.to_csv(path + '\\' + 'combine_csv.csv', index = False)
        st.write('## Nối file CSV xong!')
        st.write('#### Đường dẫn lưu file')
        st.write(path)
    else:
        shop.to_csv(path_op + '\\' + 'combine_csv.csv', index = False)
        st.write('## Nối file CSV xong!')
        st.write('#### Đường dẫn lưu file')
        st.write(path_op)
else:
    st.write('## Không tìm thấy link folder chứa file CSV')