from nameko.rpc import rpc
import uuid
from dependencies.database import DatabaseProvider
import os


class FileService:

    name = 'file_service'
    database = DatabaseProvider()

    @rpc
    def get_all_files_by_news_id(self, news_id):
        return self.database.get_files_by_news_id(news_id)

    @rpc
    def post_file(self, news_id, file_name_datastring_pairs):
        for file_name, file_string in file_name_datastring_pairs:
            generated_file_uuid = uuid.uuid1()
            open(f"/files/{generated_file_uuid}", "w").write(file_string)
            self.database.add_new_file(news_id, file_name, generated_file_uuid)

    @rpc
    def delete_all_files_from_news_id(self, news_id):
        all_files = self.database.get_files_by_news_id(news_id)

        for file in all_files:
            try:
                os.remove(f"/files/{file['filepath']}")
            except:
                continue

        self.database.delete_all_files_from_news_id(news_id)
