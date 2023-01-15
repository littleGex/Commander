import os
import subprocess
import logging


class Supporting:
    @staticmethod
    def read_write(active_item: str):
        if os.path.isfile(active_item):
            print(active_item)
            try:
                os.system("open " + active_item)
                logging.info(f"{active_item} opened for editing")
            except OSError as error:
                logging.error(error)
        # if os.path.isfile(active_item):
        #     try:
        #         subprocess.run(['open', active_item], check=True)
        #         logging.info(f"{active_item} opened for editing")
        #     except OSError as error:
        #         logging.error(error)
