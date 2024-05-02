from app.models import SankMerch, SankMerchTranslations, Size
from sqlalchemy import select
from sqlalchemy.orm import joinedload, Load
from app.database import db_session, engine


# Gather all data from queries and create the dictionary afterwards
def query_merch_and_convert_to_dict():
    # Create query strings
    sql_merch_string = "SELECT * FROM sank_merch"
    sql_image_string = "SELECT * FROM image"
    sql_merch_translation_string = "SELECT * FROM sank_merch_translations"
    sql_size_string = "SELECT * FROM size"

    with engine.connect() as conn:
        # query data
        merch_sql = conn.execute(sql_merch_string).fetchall()
        merch_translation_sql = conn.execute(sql_merch_translation_string).fetchall()
        sizes_sql = conn.execute(sql_size_string).fetchall()
        images_sql = conn.execute(sql_image_string).fetchall()

        # convert to dictionary
        merch = [{column: value for column, value in rowproxy.items()} for rowproxy in merch_sql]
        merch_translation = [{column: value for column, value in rowproxy.items()} for rowproxy in merch_translation_sql]
        sizes = [{column: value for column, value in rowproxy.items()} for rowproxy in sizes_sql]
        images = [{column: value for column, value in rowproxy.items()} for rowproxy in images_sql]

        # check if matching item id, then add it to the dictionary
        for index, item in enumerate(merch):
            # declare one to many arrays
            merch[index]['translations'] = {}
            merch[index]['sizes'] = {}
            merch[index]['images'] = []

            # gather all items for each item id
            for translation in merch_translation:
                if translation['merch_id'] == item['id']:
                    language = translation['language']
                    merch[index]['translations'][language] = translation
            for size in sizes:
                if size['merch_id'] == item['id']:
                    language = size['language']
                    if language not in merch[index]['sizes']:
                        merch[index]['sizes'][language] = []
                    merch[index]['sizes'][language].append(size)
            for image in images:
                if image['merch_id'] == item['id']:
                    merch[index]['images'].append(image)
        return merch
