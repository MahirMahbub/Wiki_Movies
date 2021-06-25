from app.create_data import CreateData
from app.cruds.data_loader import DataLoaderCrud
from app.main import db

if __name__ == '__main__':
    CreateData.get_instance().get_chain_of_responsibility()
    DataLoaderCrud(session=db).update_status(activity_name="Movie Data Loading", status=False)
    db.commit()