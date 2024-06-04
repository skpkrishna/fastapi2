from datetime import datetime
from app.models import Compute
from app.database import SessionLocal, engine
from app.calculations import calculate
from app import models
import logging

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db=get_db()

class ComputeController:
    def get_all_data():
        results = None
        try:
            results=db.query(Compute).all()
        except Exception as e:
            logger.error(f"Unable to fetch the results: {str(e)}")
        return results
    
    def get_data(id: str):
        data = None
        try:
            data=db.query(Compute).filter(Compute.batch_id==id).first()         
        except Exception as e:
            logger.error(f"Unable to fetch the results: {str(e)}")
        return data

    def create(self, batch_id: str, payload: list):
        self.start = None
        self.output = None
        self.end = None
        self.batch_id = batch_id
        self.input = payload
        self.output = None
        print(payload)
        try:
            self.start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.output = calculate(payload)
            self.end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            logger.error(f"Unable to Compute {str(e)}")

        try: 
            new_entry=Compute(
                batch_id=self.batch_id,
                input=str(self.input),
                output=str(self.output),
                created_at=self.start
            )
            db.add(new_entry)
            db.commit()
        except Exception as e:
            logger.error(f"Unable to add db entry {str(e)}")
            return {
                'batch_id': self.batch_id,
                'response': [],
                'status': "failed",
                "started_at": str(self.start),
                "completed_at": ""
            }
        return {
            'batch_id': self.batch_id,
            'response': self.output,
            'status': "complete",
            "started_at": str(self.start),
            "completed_at": str(self.end)
        }

