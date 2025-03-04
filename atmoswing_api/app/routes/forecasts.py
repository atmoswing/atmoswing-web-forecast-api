import logging
from functools import lru_cache
from fastapi import APIRouter, HTTPException, Depends
from typing_extensions import Annotated

import config
from app.models.forecast import AnalogValues, AnalogDates, AnalogCriteria
from app.services.forecasts import get_analog_values, get_analog_dates, \
    get_analog_criteria

router = APIRouter()


@lru_cache
def get_settings():
    return config.Settings()


# Helper function to handle requests and catch exceptions
async def _handle_request(func, settings: config.Settings, region: str, **kwargs):
    try:
        return await func(settings.data_dir, region, **kwargs)
    except FileNotFoundError:
        logging.error(f"Files not found for region: {region}")
        raise HTTPException(status_code=404, detail="Region or forecast not found")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{region}/{forecast_date}/{method}/{configuration}/{target_date}/dates",
            summary="Analog dates for a given forecast",
            response_model=AnalogDates)
async def analog_dates(
        region: str,
        forecast_date: str,
        method: str,
        configuration: str,
        target_date: str,
        settings: Annotated[config.Settings, Depends(get_settings)]):
    """
    Get the analog dates for a given region, forecast_date, method, configuration, and target_date.
    """
    return await _handle_request(get_analog_dates, settings, region,
                                 forecast_date=forecast_date, method=method,
                                 configuration=configuration, target_date=target_date)


@router.get("/{region}/{forecast_date}/{method}/{configuration}/{target_date}/criteria",
            summary="Analog criteria for a given forecast",
            response_model=AnalogCriteria)
async def analog_criteria(
        region: str,
        forecast_date: str,
        method: str,
        configuration: str,
        target_date: str,
        settings: Annotated[config.Settings, Depends(get_settings)]):
    """
    Get the analog criteria for a given region, forecast_date, method, configuration, and target_date.
    """
    return await _handle_request(get_analog_criteria, settings, region,
                                 forecast_date=forecast_date, method=method,
                                 configuration=configuration, target_date=target_date)


@router.get(
    "/{region}/{forecast_date}/{method}/{configuration}/{entity}/{target_date}/values",
    summary="Analog values for a given entity",
    response_model=AnalogValues)
async def analog_values(
        region: str,
        forecast_date: str,
        method: str,
        configuration: str,
        entity: int,
        target_date: str,
        settings: Annotated[config.Settings, Depends(get_settings)]):
    """
    Get the precipitation values for a given region, forecast_date, method, configuration, entity, target_date.
    """
    return await _handle_request(get_analog_values, settings, region,
                                 forecast_date=forecast_date, method=method,
                                 configuration=configuration, entity=entity,
                                 target_date=target_date)
