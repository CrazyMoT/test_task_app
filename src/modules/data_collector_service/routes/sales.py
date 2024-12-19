from fastapi import APIRouter, HTTPException
from modules.data_collector_service.config import settings
from modules.data_collector_service.logger import logger

from modules.common.schemas.schemas import Sale
from modules.common.services.kafka_producer import KafkaProducerService

router = APIRouter()

kafka_service = KafkaProducerService(settings=settings)

@router.post("/send_data")
async def collect_sales(sale: Sale):
    try:
        sale_data = sale.model_dump_json()
        trx_id = str(sale.transaction_id).encode('utf-8')
        kafka_service.send(trx_id, sale_data)
        logger.info(f"Message sent to Kafka")
        return {"status": "success", "message": "Sale data sent to Kafka"}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
