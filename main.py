import os,time,glob,datetime
from multiprocessing import Process

file_offset = {}

def follow(file_path,arguments):
    try:
        def newrelic_push(message):
            print(message)
        if file_path not in file_offset:
            with open(file_path,'r') as fh:
                fh.seek(0,os.SEEK_END)
                file_offset[file_path]=fh.tell()
        while True:
            with open(file_path,'r') as f:
                current_size = os.stat(file_path).st_size
                if current_size < file_offset[file_path]:
                    file_offset[file_path]=0
                f.seek(file_offset[file_path])
                latest_data = f.read()
                file_offset[file_path] = f.tell()
                if latest_data:
                    newrelic_push(latest_data.strip("\n"))
            time.sleep(0.2)
    except Exception as e:
        file_offset[file_path] = 0
        print(e)

def logging_monitor(logging_yml_data):
    file_process = {}
    while True:
        files_to_monitor={}
        for data in logging_yml_data:
            file_paths = glob.glob(logging_yml_data[data]["path"])
            for i in file_paths:
                files_to_monitor[i] = logging_yml_data[data]["attributes"]
        for file_path in files_to_monitor:
            if (file_path not in file_process) or ((file_path in file_process) and (not file_process[file_path].is_alive())):
                last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                current_time = datetime.datetime.fromtimestamp(time.time())
                time_elapsed = current_time - last_modified
                if time_elapsed > 0:
                    file_process[file_path] = Process(target=follow,args=(file_path,files_to_monitor[file_path],))
                    file_process[file_path].start()
        time.sleep(0.5)

if __name__ ==  '__main__':
    logging_yml_data = {
        "test1" :  {
            "path" : "E:\\logging\\*.txt",
            "attributes" : {
                "name":"test1"
            }
        },
        "test2" :  {
            "path" : "E:\\logging\\main.py",
            "attributes" : {
                "name":"main"
            }
        }
    }
    logging_monitor(logging_yml_data)
