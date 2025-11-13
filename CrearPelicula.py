import boto3
import uuid
import os
import json

def log_info(datos):
    print(json.dumps({
        "tipo": "INFO",
        "log_datos": datos
    }))

def log_error(datos):
    print(json.dumps({
        "tipo": "ERROR",
        "log_datos": datos
    }))

def lambda_handler(event, context):
    try:
        # Log de entrada
        log_info({"evento_recibido": event})

        tenant_id = event["body"]["tenant_id"]
        pelicula_datos = event["body"]["pelicula_datos"]
        nombre_tabla = os.environ["TABLE_NAME"]

        uuidv4 = str(uuid.uuid4())
        pelicula = {
            "tenant_id": tenant_id,
            "uuid": uuidv4,
            "pelicula_datos": pelicula_datos
        }

        # Guardar en DynamoDB
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log de salida
        log_info({"pelicula_guardada": pelicula})

        return {
            "statusCode": 200,
            "pelicula": pelicula,
            "response": response
        }

    except Exception as e:
        # Log de error
        log_error({"mensaje": str(e)})
        return {
            "statusCode": 500,
            "error": str(e)
        }

