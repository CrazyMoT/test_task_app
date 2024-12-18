from fastapi import APIRouter, HTTPException
from config import settings
from shared.schemas.schemas import Sale
from shared.kafka_producer import KafkaProducerService

router = APIRouter()

kafka_service = KafkaProducerService(settings=settings)

@router.post("/send_data")
async def collect_sales(sale: Sale):
    try:
        sale_data = sale.model_dump_json()
        kafka_service.send(sale.transaction_id, sale_data)
        return {"status": "success", "message": "Sale data sent to Kafka"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
