import pandas as pd
import os

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                clear_folder(file_path)
                os.rmdir(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def data_segmentation(file_name):
    df = pd.read_csv(start_path + '/' + file_name, index_col=0)
    df['date'] = pd.to_datetime(df['date']).values.astype('datetime64[D]')
    df_train = df[df['date']<=end_date]
    df_train[df_train['date']>=start_date].to_csv(end_path_1 + '/' + file_name)
    df_test = df[df['date']>end_date]
    df_test.to_csv(end_path_2 + '/' + file_name)

if __name__ == '__main__':
    start_path = 'data'
    end_path_1 = 'train set'
    end_path_2 = 'test set'
    start_date = '2012-01-01'
    end_date = '2019/12/31'

    # 清除文件夹内文件
    if not os.path.exists(end_path_1):
        # 创建目标文件夹
        os.makedirs(end_path_1)
    else:
        # 清除文件夹内文件
        clear_folder(end_path_1)

    # 清除文件夹内文件
    if not os.path.exists(end_path_2):
        # 创建目标文件夹
        os.makedirs(end_path_2)
    else:
        # 清除文件夹内文件
        clear_folder(end_path_2)

    files = os.listdir(start_path)
    
    for file in files:
        data_segmentation(file)