import os,time,glob
from multiprocessing import Process

def follow(file_path,arguments):
    try:
        def newrelic_push(message):
            print(message)
        with open(file_path,'r') as fh:
            fh.seek(0,os.SEEK_END)
            p=fh.tell()
        while True:
            with open(file_path,'r') as f:
                current_size = os.stat(file_path).st_size
                f.seek(p)
                latest_data = f.read()
                p = f.tell()
                if current_size < p:
                    p=0
                if latest_data:
                    newrelic_push(latest_data.strip("\n"))
            time.sleep(0.2)
    except Exception as e:
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
