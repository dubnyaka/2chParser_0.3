import requests,json,os,time,re,shutil

link = input('example: https://2ch.hk/***/res/******.html#******\nLink: ').replace('html','json')
x = 0
while x != 1:
    try:
        test_link = requests.get(link)
        x = 1
    except:
        print('Error: wrong link')
        link = input('example: https://2ch.hk/***/res/******.html#******\nLink: ').replace('html','json')
del test_link


x = 0
while x != 1:
    try:
        uptime = float(input('\nexample 1.0 - 1 seconds\nUptime: '))
        x = 1
    except:
        print('Error: wrong uptime')
del x

def parser():

    # Main DataBase
    check_main = {
    }
    # Create folder
    folder_name = re.sub(r"[:/]", ".", link)
    try:
        os.mkdir(folder_name)
    except:
        pass
    try:
        os.mkdir(f'{folder_name}/files')
    except:
        pass
    try:
        os.mkdir(f'{folder_name}/deletedfiles')
    except:
        pass

    #Variables




    while True:
        response = requests.get(link)
        try:
            thread_json = json.loads(response.text)
        except:
            print('Error: The link was changed!')
            break
        threads_block0 = thread_json.get('threads')
        arr_threads = threads_block0[0].get('posts')

        check_temp = {
        }

        start = time.perf_counter()
        for thread in arr_threads:
            files = thread.get('files')

            if len(files) == 0:
                continue
            else:
                for file in files:
                    file_fullname = file.get('fullname')
                    file_patch = file.get('path')

                    check_temp[file_fullname] = '0'
                    # Download file
                    if not os.path.exists(f'{folder_name}/files/{file_fullname}'):
                        try:
                            with open(f'{folder_name}/files/{file_fullname}', 'xb') as file:
                                file_bytes = requests.get(f'http://2ch.hk{file_patch}').content
                                file.write(file_bytes)
                                print(f'\nDownload file: {file_fullname}',end='\r')
                        except FileExistsError:
                            pass
        end = time.perf_counter()
        print(f'Tread size: {len(arr_threads)} Speed: ({int((1/(end-start))*len(arr_threads))} posts/s)', end='\r',flush=True)

        # Deleted files logs
        deletedarr = []
        for file in check_main:
            if not file in check_temp:
                deletedarr.append(file)
        if len(deletedarr) != 0:
            try:
                with open(f'{folder_name}/deleted.txt', 'w') as deleted_files:
                    deleted_files.write(f'{link}\nDeleted files: \n')
                    for del_files in deletedarr:
                        deleted_files.write(f'{del_files}\n')
            except:
                print('Write error')


        check_main.update(check_temp)
        # Checking for compliance
        directory = f'{folder_name}/files'
        files = os.listdir(directory)
        x = 0
        while x != len(files):
            check_main[files[x]] = '0'
            x += 1

        # Copy deleted files from /files to /deletedfiles
        if len(deletedarr) != 0:
            for del_files in deletedarr:
                if not os.path.exists(f'{folder_name}/deletedfiles/{del_files}'):
                    try:
                        shutil.copy2(fr'{folder_name}/files/{del_files}', fr'{folder_name}/deletedfiles')
                    except:
                        pass

        time.sleep(uptime)

######MAIN######

try:
    parser()
except KeyboardInterrupt:
    pass




