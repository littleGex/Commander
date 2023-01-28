import os
import shutil
import logging


class Supporting:
    @staticmethod
    def read_write(active_item: str):
        """
        This function opens the selected file for editing.

        :param active_item: File to open
        """
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

    @staticmethod
    def zip_it(active_item: str):
        """
        This function attempts to zip the user selected item.

        :param active_item: Item to zip
        """
        try:
            base = os.path.basename(active_item)
            name = base.split('.')[0]
            format_type = 'zip'

            archive_from = os.path.dirname(active_item)
            archive_to = os.path.basename(active_item.strip(os.sep))
            destination = os.path.join(archive_from, name + '.' + format_type)

            shutil.make_archive(name, format_type, archive_from, archive_to)
            shutil.move(f"{name}.{format_type}", destination)

            logging.info(f"Zip file {destination} created")
        except OSError as error:
            logging.error(error)
