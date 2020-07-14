from qbittorrent import Client

def start_download(save_path, torrent_file_path):
    # connect to the qbittorent Web UI
    qb = Client("http://127.0.0.1:8090/")

    # put the credentials (as you configured)
    qb.login("admin", "adminadmin")

    # open the torrent file of the file you wanna download
    torrent_file = open(torrent_file_path, "rb")
    print("opened file")
    print(torrent_file)
    # you can specify the save path for downloads
    qb.download_from_file(torrent_file, savepath=save_path)
    print("saved file")

