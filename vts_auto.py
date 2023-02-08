import datetime
import glob
import os
import requests
from pathlib import Path


host = "http://127.0.0.1"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
headers_for_file = {'Content-Type': 'multipart/form-data'}
ports_all = [4000]
# ports_all = range(9801, 9817)


def done():
    # is_done(True)
    print("Done!")


def edit_cell(ports, field, value):
    succeed = 0
    count_all = 0
    try:
        for port in ports:
            count = requests.get(f"{host}:{port}/data/get_count?colname=isValid").json()["count"]
            count_all += count
            print(f"VTS on port {port} contain {count} rows")
            for i in range(count):
                if requests.post(f"{host}:{port}/data/edit_cell", headers=headers,
                                 data=f"key={field}&value={value}&{field}={value}&id={i}&oper=edit").json()["success"]:
                    succeed += 1
        print(f"Changed {succeed} cells to '{value}' titled '{field}'")
        print(f"Total rows: {count_all}")
    finally:
        done()


def backup(ports):
    try:
        path = os.path.join(os.getcwd(), "backups", str(datetime.datetime.now()).replace(":", ".")[:-7])
        Path(path).mkdir(parents=True, exist_ok=True)
        print(f"Backup is saved to: {path}")
        for port in ports:
            r = requests.get(f"{host}:{port}/data/export_csv")
            with open(os.path.join(path, str(port)) + ".csv", "wb") as f:
                f.write(r.content)
    finally:
        done()


def restore(ports):
    backups_path = glob.glob(os.path.join(os.getcwd(), "backups", "*/"))
    latest_backup_path = max(backups_path, key=os.path.getmtime)
    backup_list = os.listdir(latest_backup_path)
    for file in backup_list:
        port = int(str(file)[:-4])
        if port in ports:
            file_path = os.path.join(latest_backup_path, file)
            f = {f'fileToUpload': open(file_path, "rb")}
            # per = requests.post(f"{host}:{port}/data/import_csv", files=f).request.body.decode('utf-8')
            # print(per)
            if requests.get(f"{host}:{port}/data/delete_all").json()["success"]:
                p = requests.post(f"{host}:{port}/data/import_csv", files=f).json()["success"]
                print(f'Restored to port {port}: {p}')
            pass


def main():
    # edit_cell(ports_all, "isValid", "Y")

    # backup(ports_all)
    restore(ports_all)


if __name__ == '__main__':
    main()
